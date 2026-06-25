# pinned-in-rail — Agent Notes

**Version:** 1.0.2 · **Status:** Working (CSS-only)

## Goal

When a workspace’s pinned section is collapsed (`zen-workspace[collapsedpinnedtabs]`), keep **all loaded (non-pending) pinned tab icons** visible in the rail — even when a normal tab is selected.

## Dependency

[`zen-sidebar-expand-on-hover` GVR fork](https://github.com/froggabriel/zen-sidebar-expand-on-hover) (separate repo). User runs the GVR companion stack documented in root `README.md`.

## Root cause (why Zen hides pins)

`gZenFolders.animateCollapse` on workspace collapsible pins:

- If a pinned tab is selected: `selectedTabs.length > 0`, spacer `marginTop → 0`, non-selected tabs get WAAPI `height:0; opacity:0`.
- If a **normal** tab is selected: `selectedTabs.length === 0`, `.space-fake-collapsible-start` gets large **negative `marginTop`** (inline via WAAPI), pushing icons above the clip boundary.

Older NOTES claimed JS was required to beat `hidden="true"` on the vbox. **Current fix does not need JS** — scope on `zen-workspace[collapsedpinnedtabs]` and override spacer margins with `margin-top: 0 !important` (beats inline WAAPI margins).

## What the CSS does (four cases)

| Case | Selector gist | Effect |
|------|---------------|--------|
| A | `vbox.zen-workspace-pinned-tabs-section .tabbrowser-tab:not([pending], [zen-glance-tab])` | `height/opacity: unset/1` — undo WAAPI hide on loaded tabs |
| B | `zen-workspace[collapsedpinnedtabs] … .zen-tab-group-start` | `margin-top: 0 !important` — reset folder spacers |
| C | same + `.tab-group-label-container` | `height: 0; overflow: hidden` — no folder labels in rail |
| D | same + `[pending="true"]` | zero height — hide unloaded tabs |
| E | same + `zen-folder .tab-group-container` tab/background | full width — undo expand-on-hover `calc(expanded - 28px)` folder indent |

## Case E (folder pinned tab width)

When pins section is collapsed, pinned-in-rail flattens folder tabs (e.g. Gmail inside a pinned folder) to the same width as top-level pinned / normal tabs. expand-on-hover sets `zen-folder .tab-group-container .tabbrowser-tab { width: calc(expanded - 28px) }` for folder label indent — Case E overrides to `width: 100%` on container + tabs and `-moz-available` on `.tab-background`.

## Critical lessons

1. **Never guard with `:root:not([zen-sidebar-expanded])`** when expand-on-hover is active — that attribute may be set even in the visual rail, silently killing rules.
2. **Scope on `zen-workspace[collapsedpinnedtabs]`** for B/C/D; Case A applies whenever pins are in the pinned section (works with animation cleanup).
3. **Exclude `[zen-glance-tab="true"]`** in Case A — otherwise glance tabs break.

## Not in scope

- Does not fix nested-folder icon slivers in rail (see `pin-align`, expand-on-hover clip-path model).
- Does not add tile backgrounds (`tab-containers`).

## Verify

1. Collapse workspace pinned section with a **normal** tab selected → all loaded pin icons visible.
2. Pending pins hidden; folder labels hidden.
3. With expand-on-hover: pins stay visible when sidebar is collapsed and not hovered.
