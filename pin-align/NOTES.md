# pin-align — Agent Notes

**Version:** 1.0.2 · **Status:** Working

## Goal

When the workspace pinned section is collapsed (`zen-workspace[collapsedpinnedtabs]`), **folder pinned tabs** align with top-level pinned tabs — no `-14px` translate, no hover shift from expand-on-hover folder chrome.

## Dependency

- `zen-sidebar-expand-on-hover` (folder containers use `translateX(-14px)` and padding for label space when pins are “expanded” visually).
- Works with `pinned-in-rail` (pins visible when section collapsed).

## Mechanism

All rules inside `@media (-moz-bool-pref: "zen.view.sidebar-expanded")` — expand-on-hover keeps sidebar logically expanded.

**When pins section is open** (`:not([collapsedpinnedtabs])`):

- Set `--zen-folder-indent: 14px` on folder `.tabbrowser-tab` (original indent fix).

**When pins section collapsed** (`[collapsedpinnedtabs]`):

- Zero `margin-inline-start` on `zen-folder` and `.tab-group-container > *`
- `transform: translateX(0) !important` on `.tab-group-container` (both left/right sidebar variants)
- Zero extra padding on the side where folder labels would sit

## Critical lessons

1. expand-on-hover’s `-14px` offset is for **visible folder labels**, not collapsed rail.
2. Block **hover** from re-adding `margin-inline-start` on folder containers.
3. Right-side sidebar: mirror padding (`padding-inline-start` vs `end`).

## Not in scope

- Flattening nested folder depth in rail (would need opinionated “flat rail” mod).
- Normal (unpinned) tab alignment — see `tab-containers`.

## Verify

1. Collapse workspace pins; open a pinned folder.
2. Folder child icons line up with Gmail/GitHub-style top-level pins.
3. Hover sidebar to expand — icons should not jump horizontally before expand completes.
