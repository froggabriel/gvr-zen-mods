# rail-selected-ring — Agent Notes

**Version:** 1.3.3 · **Status:** ship

## Goal

Collapsed rail only: subtle tile backgrounds + selected discernment via inset cap pseudo-elements (container stripe = 4th edge when caps leave it exposed).

## Dependency

- Pairs with `tab-containers` (tile geometry) and expand-on-hover stack.
- Loads **after** `tab-containers` in `zen-themes.css`.

## Mechanism

- CSS vars on `#navigator-toolbox`: `--rail-tile-bg`, `--rail-selected-tile`, per-edge cap sizes (`--rail-cap-s-*`, `--rail-cap-u-*`)
- Selected container tabs: `::before`/`::after` + side caps use `--identity-icon-color`
- Selected non-container: neutral cap color
- Prefs in `preferences.json`: cap edges, tile tint, container color mix, `hover_match_style`

## Disable

Turn off in Zen Mods UI or omit from `install.py`.
