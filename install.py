import os
import json
import shutil
import glob
import sys

REPO_DIR = os.path.dirname(os.path.abspath(__file__))

MODS = [
    {"id": "clean-sidebar-header", "files": ["chrome.css"]},
    {"id": "pinned-in-rail", "files": ["chrome.css"]},
    {"id": "pin-align", "files": ["chrome.css"]},
    {"id": "active-first", "files": ["chrome.css", "preferences.json"]},
    {"id": "essentials-bottom", "files": ["chrome.css"]},
    {"id": "tab-containers", "files": ["chrome.css"]},
]


def load_mod(mod):
    """Merge manifest.json into mod entry — manifest is the version source of truth."""
    manifest_path = os.path.join(REPO_DIR, mod["id"], "manifest.json")
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


MODS = [load_mod(m) for m in MODS]


def refresh_zen_themes_css(profile, mod):
    """ponytail: Zen runs bundled zen-themes.css, not per-mod files — patch it on install."""
    css_path = os.path.join(profile, "chrome", "zen-themes.css")
    if not os.path.isfile(css_path):
        return

    src_css = os.path.join(REPO_DIR, mod["id"], "chrome.css")
    with open(src_css, encoding="utf-8") as f:
        css_body = f.read().strip()

    with open(css_path, encoding="utf-8") as f:
        content = f.read()

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
        content = content.rstrip() + "\n\n" + block

    with open(css_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("  Patched zen-themes.css")


def install_mod(mod):
    mod_id = mod["id"]
    src_dir = os.path.join(REPO_DIR, mod_id)

    profiles = glob.glob(os.path.expanduser("~/Library/Application Support/zen/Profiles/*"))
    if not profiles:
        print("No Zen Browser profiles found.")
        return False

    for profile in profiles:
        if not os.path.isdir(profile):
            continue

        print(f"Installing {mod_id} v{mod['entry']['version']} to profile: {os.path.basename(profile)}...")
        dest_dir = os.path.join(profile, "chrome", "zen-themes", mod_id)
        os.makedirs(dest_dir, exist_ok=True)

        for name in mod["files"]:
            src = os.path.join(src_dir, name)
            if not os.path.isfile(src):
                print(f"  Missing {src}, skipping mod.")
                return False
            shutil.copy2(src, os.path.join(dest_dir, name))
            print(f"  Copied {name}")

        themes_json_path = os.path.join(profile, "zen-themes.json")
        themes_data = {}
        if os.path.exists(themes_json_path):
            try:
                with open(themes_json_path, encoding="utf-8") as f:
                    themes_data = json.load(f)
            except Exception as e:
                print(f"  Warning: failed to read zen-themes.json ({e}). Starting fresh.")

        existing = themes_data.get(mod_id, {})
        entry = {
            "id": mod_id,
            "isLocal": True,
            "style": "chrome.css",
            "tags": [],
            "enabled": True,  # always re-enable on explicit install
            **mod["entry"],
        }
        if "preferences.json" in mod["files"]:
            entry["preferences"] = "preferences.json"
        if os.path.isfile(os.path.join(src_dir, "README.md")):
            entry["readme"] = "README.md"
        entry.setdefault("createdAt", existing.get("createdAt", "2026-06-17"))
        entry["updatedAt"] = "2026-06-17"

        themes_data[mod_id] = entry
        with open(themes_json_path, "w", encoding="utf-8") as f:
            json.dump(themes_data, f, indent=2, ensure_ascii=False)
        print(f"  Updated zen-themes.json")

        if entry.get("enabled", True):
            refresh_zen_themes_css(profile, mod)

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
        print("\nDone. Restart Zen Browser to apply changes.")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
