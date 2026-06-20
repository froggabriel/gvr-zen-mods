# tab-containers — Agent Notes

**Version:** 1.0.5 · **Status:** Known good baseline — rail tiles work; hover-exit shrink is instant

## Goal

In collapsed rail, workspace **pinned and normal** tabs get the same rounded **tile backgrounds** as essentials (not favicon-only slivers from expand-on-hover clip-path). Center favicons; hide close X in rail.

## Dependency

- **`zen-sidebar-expand-on-hover`** — required. Clips `tab:not([zen-essential]) .tab-background` to a right-side sliver when collapsed; mod inverts that in rail.
- **`essentials-bottom`** recommended — essentials as visual reference at bottom.
- Mod loads **last** in `zen-themes.css`.

## Collapsed vs expanded triggers

Mirror expand-on-hover’s two states (do **not** use `:root:not([zen-sidebar-expanded])`):

```text
Collapsed rail:  #navigator-toolbox:not(:hover, [has-popup-menu], [movingtab], [flash-popup])
                 :not(:has(#urlbar[open], toolbarbutton[open]:not(#zen-sidepanel-button)))

Expanded:        #navigator-toolbox:is(:hover, [has-popup-menu], [movingtab], [flash-popup])
                 OR :has(#urlbar[open], toolbarbutton[open]:not(#zen-sidepanel-button))
```

## What applies when

| Rules | Collapsed only | Expanded hover |
|-------|----------------|----------------|
| Tile `.tab-background` (clip-path none, colors, radius) | ✓ | ✗ |
| `width`/`max-width` on tab | collapsed calc | ✗ |
| Center `.tab-content`, zero icon margins | ✓ | ✗ |
| Hide labels, close, reset | ✓ | ✗ |
| Pinned `[zen-pinned-changed]` icon stack → relative | ✓ | ✗ |

**All tile rules are rail-only** (`:not(:hover, …)`). Never apply layout/label-hide always-on — v1.0.8 animation attempt broke expanded hover and collapsed tiles.

## Known limitation: hover-exit shrink

Tabs snap to tile mode instantly when hover ends, while `#navigator-toolbox` clip-path still animates. User wants full-width tabs + title to persist until sidebar collapse finishes (like `active-first` inactive-tab hide).

**Why CSS attempts failed (v1.0.6–1.0.8):**

| Version | Approach | Result |
|---------|----------|--------|
| 1.0.6–1.0.7 | `max-width` / margin **transitions** with `--transition-delay-smooth` or `--transition-delay-fast` | Wrong properties — only icon alignment delayed; max-width doesn’t control visible width |
| 1.0.8 | `@keyframes` + `animation-delay: --transition-delay-fast` on tile chrome | **Broken** — no tile color in rail, misaligned; animations don’t reliably hold/apply `!important` tile styles in Gecko |

**Root cause:** Tab row logical width is always `--expanded-tab-bar-width` inside `#navigator-toolbox`. Visible “full tab vs tile” is `.tab-background` clip-path + rail-only rules that **flip on `:not(:hover)` instantly**. CSS can delay *property* transitions but not *selector* application; delaying tile chrome without breaking final tile state needs JS or expand-on-hover upstream changes.

**Do not retry without new approach:** margin/icon transitions alone; always-on tile layout; `@keyframes` for tile backgrounds (v1.0.8).

## Pinned-specific

- Zen: `[zen-pinned-changed="true"]` uses `position: absolute; left: 8px` on icon stack for expanded layout.
- Rail-only rule resets to `relative` + centered in flex tab-content.

## Verify

1. **Collapsed rail:** tiles on pinned + normal; essentials match; no close X; icons centered; container colors present.
2. **Expanded hover:** full-width tabs, labels visible, close X on selected normal tabs.
3. **Hover exit:** instant tile snap (known).
