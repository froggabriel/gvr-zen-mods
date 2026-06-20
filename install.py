import os
import json
import shutil
import glob
import sys

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
EXPAND_ON_HOVER_DIR = os.path.join(os.path.dirname(REPO_DIR), "zen-sidebar-expand-on-hover")

# expand-on-hover first — gvr companion mods override its rail clip-path
MODS = [
    {
        "id": "zen-sidebar-expand-on-hover",
        "src_dir": EXPAND_ON_HOVER_DIR,
        "files": ["chrome.css", "preferences.json"],
    },
    {"id": "clean-sidebar-header", "files": ["chrome.css"]},
    {"id": "pinned-in-rail", "files": ["chrome.css"]},
    {"id": "pin-align", "files": ["chrome.css"]},
    {"id": "active-first", "files": ["chrome.css", "preferences.json"]},
    {"id": "essentials-bottom", "files": ["chrome.css"]},
    {"id": "tab-containers", "files": ["chrome.css"], "js": "rail-pending.uc.js"},
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
    """Keep existing zen-themes.json key (e.g. theme-store UUID) when names match."""
    if mod["id"] != "zen-sidebar-expand-on-hover":
        return mod["id"]
    for key, existing in themes_data.items():
        if existing.get("name") == mod["entry"]["name"] or key == mod["id"]:
            return key
    return mod["id"]


MODS = [load_mod(m) for m in MODS]

ZEN_PROFILES_DIR = os.path.expanduser("~/Library/Application Support/zen/Profiles")


def zen_profiles():
    """Install to release profile only; override with ZEN_PROFILE=substring."""
    all_profiles = [
        p for p in glob.glob(os.path.join(ZEN_PROFILES_DIR, "*")) if os.path.isdir(p)
    ]
    if not all_profiles:
        return []

    override = os.environ.get("ZEN_PROFILE")
    if override:
        matched = [p for p in all_profiles if override in os.path.basename(p)]
        return matched or all_profiles

    release = [p for p in all_profiles if "(release)" in os.path.basename(p)]
    return release or all_profiles


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


def install_rail_pending_js(profile):
    src = os.path.join(REPO_DIR, "tab-containers", "rail-pending.uc.js")
    if not os.path.isfile(src):
        return

    chrome_dir = os.path.join(profile, "chrome")
    fx_utils = os.path.join(chrome_dir, "utils", "chrome.manifest")
    if not os.path.isfile(fx_utils):
        print("  Note: optional fx-autoconfig hold script skipped (no chrome/utils/)")
        return

    js_dir = os.path.join(chrome_dir, "JS")
    os.makedirs(js_dir, exist_ok=True)
    shutil.copy2(src, os.path.join(js_dir, "tab-containers-rail-pending.uc.js"))
    print("  Installed tab-containers-rail-pending.uc.js (fx-autoconfig)")


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

        if mod["id"] == "tab-containers":
            install_rail_pending_js(profile)

    return True


def main():
    ids = sys.argv[1:] or [m["id"] for m in MODS]
    by_id = {m["id"]: m for m in MODS}
    ok = True
    for mod_id in ids:
        if mod_id not in by_id:
            print(f"Unknown mod: {mod_id}")
            ok = False
            continue
        ok = install_mod(by_id[mod_id]) and ok

    if ok:
        print("\nDone. Quit Zen (Cmd+Q), reopen, then apply.")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
