# gvr-zen-mods — Repo Notes (for agents)

## What this repo is

CSS utility mods for [Zen Browser](https://zen-browser.app) — **Zen Mods = CSS only** per [official docs](https://docs.zen-browser.app/user-manual/extensions). **Version source of truth:** each mod’s `manifest.json`. Install/uninstall via `install.py` → **Default (release)** profile → `chrome/zen-themes/<mod-id>/` + patch **`zen-themes.css`**.

## External dependency (not in this repo)

**`zen-sidebar-expand-on-hover`** — fork at `~/Repos/zen-sidebar-expand-on-hover` (froggabriel lineage). **Not installed by `install.py`** — install separately, first in the stack.

Most GVR mods are **companions** that fix rail UX on top of that model.

## Recommended ship stack (order matters in zen-themes.css)

1. expand-on-hover (external)
2. pinned-in-rail
3. pin-align
4. essentials-bottom
5. tab-containers
6. rail-selected-ring (last)

Optional: `active-first`, `clean-sidebar-header` (independent).

## Cross-cutting rules (do not forget)

1. **Never use `:root:not([zen-sidebar-expanded])`** as collapsed-rail guard when expand-on-hover is active — attribute may be set while visually collapsed.
2. **Collapsed vs expanded triggers** must mirror expand-on-hover:
   - Collapsed: `#navigator-toolbox:not(:hover, [has-popup-menu], [movingtab], [flash-popup]):not(:has(#urlbar[open], toolbarbutton[open]:not(#zen-sidepanel-button)))`
   - Expanded: `:is(:hover, …)` or `:has(#urlbar[open], …)`
3. **Timing vars** on `#navigator-toolbox`: `--transition-duration`, `--transition-delay-after`, `--transition-delay-smooth`, `--collapsed-tab-bar-width`, `--expanded-tab-bar-width`.
4. **Zen folders** (`zen-folder`, `zen-workspace[collapsedpinnedtabs]`) are first-class in current Zen — not “missing Arc folders”.
5. **ponytail rule:** minimal diffs; mark intentional shortcuts; one runnable check for non-trivial logic.

## Install

```bash
python3 install.py              # all mods
python3 install.py tab-containers   # one mod
```

Restart Zen after install.

**Profile:** `install.py` reads Zen’s `profiles.ini` (default install profile). Override: `ZEN_PROFILE=substring` (name or path) or `ZEN_PROFILE_PATH=/full/path`. Debug: `python3 install.py --profile`.

## Per-mod deep dives

Each mod directory has its own `NOTES.md`. Start with `tab-containers/NOTES.md` for rail work.

**Manual QA:** [`TESTING.md`](TESTING.md) — P0/P1 checklist for the ship stack (run before merge).

## Git history

- **`main`** / **`main-pre-squash-20260620`**: full 85-commit history at `014511a` (`ship` tag).
- **`squash-work-v3`**: 12-commit rewrite (11 feature + docs); not merged to `main` yet.
- Golden discovery commits tagged on backup branch — see `tab-containers/NOTES.md`.

## TODO (unfixed)

- **Folder rename + expand-on-hover:** Create folder → typing name → mouse leaves sidebar → sidebar collapses while input active.

## User UX target (context)

Arc/Edge-style **icon dock** in collapsed rail: essentials at bottom, workspace tabs with tile backgrounds, pins visible when section collapsed, full sidebar on hover. This stack is a mod-based answer to community sidebar rail threads.
