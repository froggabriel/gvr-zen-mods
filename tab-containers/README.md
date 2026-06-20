# [GVR] Tab Containers

**Version:** 1.0.6

Keeps essentials-style tile backgrounds on workspace pinned and normal tabs in the collapsed rail.

Companion for `zen-sidebar-expand-on-hover`, which clips non-essential tab backgrounds down to favicon-only slivers when the sidebar is collapsed. Works well with `essentials-bottom`.

## Behavior

- Rounded tile backgrounds on pinned and normal workspace tabs in collapsed rail
- Tile sizing and margins match essentials
- Favicons centered within each tile
- Tab width eases with sidebar collapse (expand-on-hover delay + duration)
- Tab close button hidden in collapsed rail (returns when the sidebar expands on hover)

## Install

From the repo root:

```bash
python3 install.py tab-containers
```

Restart Zen Browser to apply.
