# active-first — Agent Notes

**Version:** 1.0.0 · **Status:** Working

## Goal

- **Rail (collapsed):** Active unpinned tabs stay visible; inactive unpinned tabs hidden (default) or sorted below (`order: 999`).
- **Expanded (hover):** Inactive tabs revealed immediately; hidden again **after** sidebar finishes collapsing.

## Dependency

- `zen-sidebar-expand-on-hover` — provides `--transition-duration`, `--transition-delay-after`, `--transition-delay-smooth`, and hover triggers.
- Pref namespace: `mod.gvr-active-tabs-first.*` (see `preferences.json`).

## Mechanism

Guard: `@media (-moz-bool-pref: "zen.view.sidebar-expanded")` — matches expand-on-hover’s logical expanded layout.

**Always:** `tab[pending="true"]:not([zen-essential]):not([pinned]) { order: 999 }` — sleeping tabs sink in the list.

**When `mod.gvr-active-tabs-first.hide_inactive_in_rail` is true (default):**

| State | Trigger | Effect |
|-------|---------|--------|
| Rail | default | `max-height: 0; overflow: hidden` on pending unpinned tabs |
| Rail hide delay | `transition` | `calc(var(--transition-delay-after) + var(--transition-duration))` — hide **after** collapse animation |
| Expanded | `#navigator-toolbox:is(:hover, …)` or urlbar/button open | `max-height: 35px`, transition delay `0ms` |

## Critical lessons

1. **Timing pattern to copy:** hide after collapse = `delay-after + duration`; reveal on expand = `0ms` delay. Same pattern attempted in `tab-containers`.
2. `[pending="true"]` = Zen’s unloaded/sleeping tab state, not “user pending pin”.
3. Does not affect pinned or essentials tabs.

## Verify

1. Rail: only active normal tab(s) visible among unpinned tabs.
2. Hover expand: sleeping tabs appear at bottom of section.
3. Unhover: sleeping tabs disappear only after collapse delay + animation.
