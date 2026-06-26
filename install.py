import os
import json
import shutil
import sys
from configparser import ConfigParser
from pathlib import Path

REPO_DIR = os.path.dirname(os.path.abspath(__file__))

# Load order in zen-themes.css matters — tab-containers before rail-selected-ring
MODS = [
    {"id": "clean-sidebar-header", "files": ["chrome.css"]},
    {"id": "pinned-in-rail", "files": ["chrome.css"]},
    {"id": "pin-align", "files": ["chrome.css"]},
    {"id": "active-first", "files": ["chrome.css", "preferences.json"]},
    {"id": "essentials-bottom", "files": ["chrome.css"]},
    {"id": "tab-containers", "files": ["chrome.css", "preferences.json"]},
    {"id": "rail-selected-ring", "files": ["chrome.css", "preferences.json"]},
]


def mod_src_dir(mod):
    return mod.get("src_dir", os.path.join(REPO_DIR, mod["id"]))


def load_mod(mod):
    """Merge manifest.json into mod entry — manifest is the version source of truth."""
    manifest_path = os.path.join(mod_src_dir(mod), "manifest.json")
    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)
    return {
        **mod,
        "entry": {
            "name": manifest["name"],
            "description": manifest["description"],
            "author": manifest["author"],
            "version": manifest["version"],
        },
    }


def resolve_themes_key(themes_data, mod):
    """Keep existing zen-themes.json key when id or display name matches."""
    for key, existing in themes_data.items():
        if key == mod["id"] or existing.get("name") == mod["entry"]["name"]:
            return key
    return mod["id"]


MODS = [load_mod(m) for m in MODS]


def zen_data_roots():
    """Zen app-data dirs that contain profiles.ini (Firefox-style layout)."""
    home = Path.home()
    candidates = []
    if sys.platform == "darwin":
        candidates.append(home / "Library/Application Support/zen")
    elif sys.platform == "win32":
        appdata = os.environ.get("APPDATA")
        if appdata:
            candidates.append(Path(appdata) / "zen")
    else:
        candidates.extend(
            [
                home / ".var/app/app.zen_browser.zen/.zen",
                home / ".config/zen",
                home / ".zen",
            ]
        )
    return [p for p in candidates if (p / "profiles.ini").is_file()]


def profiles_from_ini(data_root):
    """Return profile entries from profiles.ini: name, path (absolute), is_default."""
    ini = ConfigParser()
    ini.read(data_root / "profiles.ini", encoding="utf-8")

    install_default = None
    for section in ini.sections():
        if section.startswith("Install") and ini.has_option(section, "Default"):
            install_default = ini.get(section, "Default")
            break

    profiles = []
    for section in ini.sections():
        if not section.startswith("Profile"):
            continue
        rel = ini.get(section, "Path", fallback="")
        if not rel:
            continue
        is_relative = ini.get(section, "IsRelative", fallback="1") == "1"
        path = (data_root / rel).resolve() if is_relative else Path(rel).expanduser().resolve()
        name = ini.get(section, "Name", fallback=path.name)
        is_default = ini.get(section, "Default", fallback="0") == "1"
        profiles.append({"name": name, "path": str(path), "default": is_default})

    default_path = None
    if install_default:
        default_path = str((data_root / install_default).resolve())
    elif profiles:
        marked = [p["path"] for p in profiles if p["default"]]
        default_path = marked[0] if marked else None

    return profiles, default_path


def zen_profiles():
    """Resolve install target(s) from profiles.ini; override with env vars."""
    explicit = os.environ.get("ZEN_PROFILE_PATH")
    if explicit:
        path = Path(explicit).expanduser()
        if path.is_dir():
            return [str(path.resolve())]
        print(f"ZEN_PROFILE_PATH not found: {path}")
        return []

    roots = zen_data_roots()
    if not roots:
        return []

    all_profiles = []
    default_paths = []
    for root in roots:
        profiles, default_path = profiles_from_ini(root)
        all_profiles.extend(profiles)
        if default_path:
            default_paths.append(default_path)

    paths = [p["path"] for p in all_profiles]
    if not paths:
        return []

    override = os.environ.get("ZEN_PROFILE")
    if override:
        matched = [
            p["path"]
            for p in all_profiles
            if override in p["name"] or override in os.path.basename(p["path"])
        ]
        return matched or paths

    for dp in default_paths:
        if dp in paths:
            return [dp]

    release = [p for p in paths if "(release)" in os.path.basename(p)]
    return release or paths


def refresh_zen_themes_css(profile, mod):
    """ponytail: Zen runs bundled zen-themes.css, not per-mod files — patch it on install."""
    css_path = os.path.join(profile, "chrome", "zen-themes.css")
    os.makedirs(os.path.dirname(css_path), exist_ok=True)

    src_css = os.path.join(mod_src_dir(mod), "chrome.css")
    with open(src_css, encoding="utf-8") as f:
        css_body = f.read().strip()

    if os.path.isfile(css_path):
        with open(css_path, encoding="utf-8") as f:
            content = f.read()
    else:
        content = ""

    name = mod["entry"]["name"]
    desc = mod["entry"]["description"]
    author = mod["entry"]["author"]
    marker = f"/* Name: {name} */"
    block = f"{marker}\n/* Description: {desc} */\n/* Author: @{author} */\n{css_body}\n"

    if marker in content:
        start = content.index(marker)
        rest = content[start + len(marker) :]
        next_idx = rest.find("\n/* Name: ")
        end = start + len(marker) + (next_idx if next_idx != -1 else len(rest))
        content = content[:start] + block + content[end:]
    else:
        end_marker = "/* End of Zen Mods */"
        if end_marker in content:
            content = content.replace(end_marker, block + "\n" + end_marker, 1)
        else:
            content = content.rstrip() + "\n\n" + block

    with open(css_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("  Patched zen-themes.css")


LEGACY_RAIL_PENDING_JS = "tab-containers-rail-pending.uc.js"


def mod_marker(mod):
    return f"/* Name: {mod['entry']['name']} */"


def remove_from_zen_themes_css(profile, mod):
    css_path = os.path.join(profile, "chrome", "zen-themes.css")
    if not os.path.isfile(css_path):
        return

    marker = mod_marker(mod)
    with open(css_path, encoding="utf-8") as f:
        content = f.read()
    if marker not in content:
        print("  Not in zen-themes.css")
        return

    start = content.index(marker)
    rest = content[start + len(marker) :]
    next_idx = rest.find("\n/* Name: ")
    end = start + len(marker) + (next_idx if next_idx != -1 else len(rest))
    content = (content[:start] + content[end:]).lstrip("\n")
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("  Removed from zen-themes.css")


def remove_legacy_rail_pending_js(profile):
    path = os.path.join(profile, "chrome", "JS", LEGACY_RAIL_PENDING_JS)
    if os.path.isfile(path):
        os.remove(path)
        print(f"  Removed {LEGACY_RAIL_PENDING_JS} (legacy fx-autoconfig)")


def uninstall_mod(mod):
    mod_id = mod["id"]
    profiles = zen_profiles()
    if not profiles:
        print("No Zen Browser profiles found.")
        return False

    for profile in profiles:
        print(f"Uninstalling {mod_id} from profile: {os.path.basename(profile)}...")

        themes_json_path = os.path.join(profile, "zen-themes.json")
        themes_data = {}
        if os.path.exists(themes_json_path):
            try:
                with open(themes_json_path, encoding="utf-8") as f:
                    themes_data = json.load(f)
            except Exception as e:
                print(f"  Warning: failed to read zen-themes.json ({e}).")

        themes_key = resolve_themes_key(themes_data, mod) if themes_data else mod_id
        if themes_key in themes_data:
            del themes_data[themes_key]
            with open(themes_json_path, "w", encoding="utf-8") as f:
                json.dump(themes_data, f, indent=2, ensure_ascii=False)
            print(f"  Removed from zen-themes.json ({themes_key})")

        for key in {themes_key, mod_id}:
            dest_dir = os.path.join(profile, "chrome", "zen-themes", key)
            if os.path.isdir(dest_dir):
                shutil.rmtree(dest_dir)
                print(f"  Removed chrome/zen-themes/{key}/")

        remove_from_zen_themes_css(profile, mod)
        if mod_id == "tab-containers":
            remove_legacy_rail_pending_js(profile)

    return True


def install_mod(mod):
    mod_id = mod["id"]
    src_dir = mod_src_dir(mod)

    profiles = zen_profiles()
    if not profiles:
        print("No Zen Browser profiles found.")
        return False

    for profile in profiles:
        print(f"Installing {mod_id} v{mod['entry']['version']} to profile: {os.path.basename(profile)}...")

        themes_json_path = os.path.join(profile, "zen-themes.json")
        themes_data = {}
        if os.path.exists(themes_json_path):
            try:
                with open(themes_json_path, encoding="utf-8") as f:
                    themes_data = json.load(f)
            except Exception as e:
                print(f"  Warning: failed to read zen-themes.json ({e}). Starting fresh.")

        themes_key = resolve_themes_key(themes_data, mod)
        dest_dir = os.path.join(profile, "chrome", "zen-themes", themes_key)
        os.makedirs(dest_dir, exist_ok=True)

        for name in mod["files"]:
            src = os.path.join(src_dir, name)
            if not os.path.isfile(src):
                print(f"  Missing {src}, skipping mod.")
                return False
            shutil.copy2(src, os.path.join(dest_dir, name))
            print(f"  Copied {name}")

        existing = themes_data.get(themes_key, {})
        entry = {
            "id": themes_key,
            "isLocal": True,
            "style": "chrome.css",
            "tags": [],
            "enabled": True,
            **mod["entry"],
        }
        # ponytail: install re-enables; Zen UI disable is for testing only
        entry["enabled"] = True
        if "preferences.json" in mod["files"]:
            entry["preferences"] = "preferences.json"
        if os.path.isfile(os.path.join(src_dir, "README.md")):
            entry["readme"] = "README.md"
        entry.setdefault("createdAt", existing.get("createdAt", "2026-06-17"))
        entry["updatedAt"] = "2026-06-17"

        themes_data[themes_key] = entry
        with open(themes_json_path, "w", encoding="utf-8") as f:
            json.dump(themes_data, f, indent=2, ensure_ascii=False)
        print(f"  Updated zen-themes.json ({themes_key})")

        if entry.get("enabled", True):
            refresh_zen_themes_css(profile, mod)

    return True


def main():
    if "--profile" in sys.argv:
        for path in zen_profiles():
            print(path)
        return

    uninstall = "--uninstall" in sys.argv
    ids = [a for a in sys.argv[1:] if a not in ("--profile", "--uninstall")]
    ids = ids or [m["id"] for m in MODS]
    by_id = {m["id"]: m for m in MODS}
    action = uninstall_mod if uninstall else install_mod
    label = "Uninstall" if uninstall else "Done"
    ok = True
    for mod_id in ids:
        if mod_id not in by_id:
            print(f"Unknown mod: {mod_id}")
            ok = False
            continue
        ok = action(by_id[mod_id]) and ok

    if ok:
        print(f"\n{label}. Quit Zen (Cmd+Q), reopen, then apply.")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
