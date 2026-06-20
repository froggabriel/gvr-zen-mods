# gvr-zen-mods — Repo Notes (for agents)

## What this repo is

CSS utility mods for [Zen Browser](https://zen-browser.app), installed via `install.py` into the **Default (release)** profile’s `chrome/zen-themes/<mod-id>/` and patched into **`zen-themes.css`** (Zen runs the bundled aggregate, not per-mod files alone).

**Version source of truth:** each mod’s `manifest.json`. `install.py` reads manifest for name/description/version and forces `"enabled": true` on explicit install.

## External dependency (not in this repo)

**`zen-sidebar-expand-on-hover`** — fork at `~/Repos/zen-sidebar-expand-on-hover` (froggabriel lineage). GVR patch: collapsed favicon margins scoped to `:not(:hover)` with `--transition-delay-fast`. Install via `python3 install.py zen-sidebar-expand-on-hover` (listed first in full install).

Most GVR mods are **companions** that fix rail UX on top of that model.

## Recommended user stack (order matters in zen-themes.css)

1. expand-on-hover (external)
2. pinned-in-rail
3. pin-align
4. active-first
5. essentials-bottom
6. tab-containers (last — overrides expand-on-hover clip-path in rail)

clean-sidebar-header is independent.

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

**Profile:** `install.py` targets `Default (release)` only. Override: `ZEN_PROFILE=substring python3 install.py …`. Do not install to every profile under `Profiles/*` — orphan profiles (e.g. old `Default Profile`) may have unrelated tooling (Sine, etc.).

## Per-mod deep dives

Each mod directory has its own `NOTES.md`.

## TODO (unfixed)

- **Folder rename + expand-on-hover:** Create folder → start typing name → mouse leaves sidebar → sidebar collapses while input is still active; user can't see what they're typing. Likely needs expand-on-hover `:hover` guard for folder rename input focus (or upstream Zen attribute). See `tab-containers/NOTES.md`.

## Unbuilt future work (not in repo)

- **`gvr-sidebar-rail`** — opinionated clean-slate mod spec (flat rail, essentials linear/mosaic). Not implemented.
- **tab-containers collapse hold** — abandoned after CSS/JS attempts; stay on v1.0.5.

## User UX target (context)

Arc/Edge-style **icon dock** in collapsed rail: essentials at bottom, workspace tabs with tile backgrounds, pins visible when section collapsed, full sidebar on hover. Community GitHub threads (#3522, #3696, #3040, PR #1757) describe the same pain; this stack is a mod-based answer.
