# gvr-zen-mods

Small CSS utility mods for [Zen Browser](https://zen-browser.app). Each rail mod is meant to be **independent and useful on its own** — install only what you need. In practice those mods share assumptions today (especially with [Sidebar Expand on Hover](https://github.com/StormAnon/zen-sidebar-expand-on-hover/tree/main)), so they work **best installed as a bundle** in the order below.

**[clean-sidebar-header](clean-sidebar-header/)** is different: no dependency on eoh or any other mod here — install it alone anytime.

![Ship stack demo — collapsed rail, hover expand, collapse](docs/demo.gif)

## Mods

| Mod | Preview | Version | Description |
|-----|---------|---------|-------------|
| [pin-align](pin-align/) | ![pin-align](pin-align/screenshot.png?v=3) | 1.0.4 | Fixes pinned folder-tab icon alignment in the collapsed rail |
| [active-first](active-first/) | ![active-first](active-first/screenshot.png?v=3) | 1.0.1 | Sorts inactive tabs to the bottom when expanded; hides them in the collapsed rail |
| [essentials-bottom](essentials-bottom/) | ![essentials-bottom](essentials-bottom/screenshot.png?v=1) | 1.0.8 | Moves essentials tabs to the bottom of the sidebar |
| [pinned-in-rail](pinned-in-rail/) | ![pinned-in-rail](pinned-in-rail/screenshot.png?v=3) | 1.0.1 | Keeps loaded pinned tabs visible in the rail when the workspace section is collapsed |
| [tab-containers](tab-containers/) | ![tab-containers](tab-containers/screenshot.png?v=1) | 1.0.60 | Tile geometry in collapsed rail; instant collapse |
| [rail-selected-ring](rail-selected-ring/) | ![rail-selected-ring](rail-selected-ring/screenshot.png?v=1) | 1.3.3 | Collapsed-rail tile tint and selected cap ring |
| [clean-sidebar-header](clean-sidebar-header/) | ![clean-sidebar-header](clean-sidebar-header/screenshot.png?v=1) | 1.0.0 | Hides the title bar in extension sidebars — **no eoh or rail dependencies** |

Registry previews are `screenshot.png` in each mod folder (600×400 PNG, per [Zen Mods submission guidelines](https://docs.zen-browser.app/themes-store/themes-marketplace-submission-guidelines)).

Companions for **Sidebar Expand on Hover** (not in this repo). Recommended bundle order (rail mods in the table above, excluding `clean-sidebar-header`):

`expand-on-hover` → `pin-align` → `active-first` → `essentials-bottom` → `pinned-in-rail` → `tab-containers` → `rail-selected-ring`

## Install

```bash
python3 install.py              # all mods in this repo
python3 install.py tab-containers   # one mod
python3 install.py --uninstall tab-containers   # remove one mod
python3 install.py --uninstall   # remove all mods from this repo
```

**Sidebar Expand on Hover** — install from the [GitHub repo](https://github.com/StormAnon/zen-sidebar-expand-on-hover) or Zen Mods UI **before** the rail companions. Individual mods: `python3 install.py <mod-id>`. See bundle order above and root `NOTES.md`.

Restart Zen Browser after installing.
