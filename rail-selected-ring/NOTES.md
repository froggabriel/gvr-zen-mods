# rail-selected-ring — Agent Notes

**Version:** 1.0.1 · **Status:** Working (3-edge ring on container tabs; stripe = 4th edge)

## Goal

Collapsed rail only (`#navigator-toolbox:not(:hover, …)`): tile backgrounds on tabs + selected discernment via inset ring, not a bright fill.

## Dependency

- Pairs with `tab-containers` (tile geometry) and expand-on-hover stack.
- Loads **after** `tab-containers` in `zen-themes.css`.

## Mechanism

- Unselected: `var(--zen-toolbar-element-bg)`
- Hover (not selected): light overlay
- Selected non-container: neutral `box-shadow` inset ring
- Selected container: `box-shadow` uses `--identity-icon-color` (Firefox contextual tab var)

## Disable

Turn off in Zen Mods UI or omit from `install.py` — `tab-containers` no longer ships selection styling.
