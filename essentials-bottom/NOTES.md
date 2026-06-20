# essentials-bottom — Agent Notes

**Version:** 1.0.3 · **Status:** Working

## Goal

Move the essentials grid to the **bottom** of the vertical sidebar (Arc-style: workspace tabs in the middle/top, favorites at the bottom).

## Dependency

- `@media (-moz-bool-pref: "zen.tabs.vertical")` — vertical tabs only.
- Pairs with `zen-sidebar-expand-on-hover` + `mod.autoexpand.essentials_vertical` (1-column essentials in rail).
- Pairs with `tab-containers` (workspace tabs get tiles; essentials already have tiles).

## Mechanism

Flex reorder inside `#tabbrowser-tabs`:

| Element | Change |
|---------|--------|
| `#zen-tabs-wrapper` | `order: 0`, `flex: 1 1 auto`, `min-height: 0` — fills middle |
| `#zen-essentials` | `order: 999`, `margin-top: auto` — sticks to bottom |
| `zen-workspace` | `padding-top: 0 !important` — Zen JS sets inline padding-top to reserve essentials height at top; must clear it |

**Horizontal bleed (v1.0.2–1.0.3 fixes):**

- `#zen-essentials`: `margin-inline: calc(-1 * var(--zen-toolbox-padding))`, `width: calc(100% + 2 * padding)` — match Zen’s symmetric toolbox bleed so essentials align with workspace tabs.
- `.zen-essentials-container`: `position: relative` (was absolute), full width, visible overflow.

## Critical lessons

1. **`ZenSpaceManager.#updatePaddingTopOnTabs`** sets inline `padding-top` on each workspace — CSS `!important` required after move.
2. Essentials container excluded from `.zen-workspace-tabs-section` horizontal padding rule in Zen — negative margin compensates.
3. Do not use `:root:not([zen-sidebar-expanded])` guards for layout that must work with expand-on-hover.

## Not in scope

- Essentials mosaic on expand (expand-on-hover pref).
- Tile styling for workspace tabs (`tab-containers`).

## Verify

1. Essentials (e.g. YouTube) at bottom of sidebar in collapsed rail.
2. No empty gap at top of workspace tab list.
3. Left/right tile edges align with workspace tabs when `tab-containers` enabled.
