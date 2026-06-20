# gvr-zen-mods

Small CSS utility mods for [Zen Browser](https://zen-browser.app).

## Mods

| Mod | Version | Description |
|-----|---------|-------------|
| [pinned-in-rail](pinned-in-rail/) | 1.0.2 | Keeps loaded pinned tabs visible in the rail when the workspace section is collapsed |
| [pin-align](pin-align/) | 1.0.2 | Fixes pinned folder-tab icon alignment in the collapsed rail |
| [active-first](active-first/) | 1.0.0 | Active tabs on top in rail; inactive hidden when expanded |
| [essentials-bottom](essentials-bottom/) | 1.0.3 | Moves essentials tabs to the bottom of the sidebar |
| [tab-containers](tab-containers/) | 1.0.5 | Tile backgrounds in collapsed rail; collapse hold via CSS animation |
| [clean-sidebar-header](clean-sidebar-header/) | 1.0.0 | Hides the title bar in extension sidebars |

`pinned-in-rail`, `pin-align`, `active-first`, `tab-containers`, and `essentials-bottom` are companions for `zen-sidebar-expand-on-hover`.

## Install

```bash
python3 install.py                              # all mods (expand-on-hover first)
python3 install.py zen-sidebar-expand-on-hover  # fork only
python3 install.py tab-containers               # one gvr mod
```

Expand-on-hover source: `~/Repos/zen-sidebar-expand-on-hover` (sibling repo, not in this tree).

Restart Zen Browser after installing.
