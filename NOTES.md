# gvr-zen-mods — Repo Notes (for agents)

## What this repo is

CSS utility mods for [Zen Browser](https://zen-browser.app) — **Zen Mods = CSS only** per [official docs](https://docs.zen-browser.app/user-manual/extensions). Installed via `install.py` into **Default (release)** → `chrome/zen-themes/<mod-id>/` + patch **`zen-themes.css`**.

**Version source of truth:** each mod’s `manifest.json`. Optional JS (`tab-containers/rail-pending.uc.js`) is fx-autoconfig only — not the Zen Mods loader path.

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

- **tab-containers:** **v1.0.51** instant collapse (snap + hide labels). #2 stripe-hold closed by user preference.
- **Folder rename + expand-on-hover:** Create folder → typing name → mouse leaves sidebar → sidebar collapses while input active.

## Learnings (2026-06 — pinned rail session)

**Ship baseline:** `tab-containers` **v1.0.49** = v1.0.46 pinned layout/hold + immediate pinned bg cap. **Fixed:** hover narrow (#1), label hold, icon in tile. **Open:** stripe snap (#2).

**Golden commits:** collapsed visuals = `4fd2ba0` (tc v1.0.5 static). Hold primary = eoh `1688c30`. tc companion = `435b945` (width/content/labels — not stripe layer).

**Stripes** = native `.tab-context-line` on `.tab-background`. Pinned stripe snap = tc immediate pinned bg cap, not label hold.

**#1 fix (v1.0.46):** row flex is inside `zen-folder .tab-group-container`, not outer pinned vbox. Essentials ≠ pinned.

**#2 dead ends:** tc global + scoped cap delay (v1.0.47–48, v1.0.50); eoh folder indent exempt (v1.0.12). **Tradeoff confirmed:** immediate cap = edge ✓ snap ✗; delayed cap = edge ✗ layout shift ✗. JS `rail-pending` only path left.

Full log: `tab-containers/NOTES.md`.

## Unbuilt future work (not in repo)

- **`gvr-sidebar-rail`** — opinionated clean-slate mod spec (flat rail, essentials linear/mosaic). Not implemented.

## User UX target (context)

Arc/Edge-style **icon dock** in collapsed rail: essentials at bottom, workspace tabs with tile backgrounds, pins visible when section collapsed, full sidebar on hover. Community GitHub threads (#3522, #3696, #3040, PR #1757) describe the same pain; this stack is a mod-based answer.
