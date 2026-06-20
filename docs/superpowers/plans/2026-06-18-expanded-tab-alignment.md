# Expanded Tab Alignment — Implementation Plan

**Goal:** Fix expanded sidebar tab alignment without breaking collapse hold.

**Architecture:** Collapsed gate on rail margin animations in expand-on-hover; minimal expand unset in tab-containers for animation forwards only.

---

### Task 1: expand-on-hover collapsed gate

**Files:** `~/Repos/zen-sidebar-expand-on-hover/chrome.css`

- [ ] Add `:not(:hover, [has-popup-menu], [movingtab], [flash-popup]):not(:has(#urlbar[open], …))` to `eoh-rail-margin-*` and `eoh-rail-icon-*` selector blocks (left + right sidebar).

### Task 2: tab-containers expand unset

**Files:** `gvr-zen-mods/tab-containers/chrome.css`

- [ ] On existing expand `:is(:hover, …)` / `:has(#urlbar[open])` rules for `.tab-content`: add `padding/display/flex/width: unset !important`
- [ ] Same for `.tab-icon-*`: `margin-inline: unset !important`
- [ ] Do **not** bump version; note experiment in `tab-containers/NOTES.md`

### Task 3: Install & verify

- [ ] `python3 install.py zen-sidebar-expand-on-hover tab-containers`
- [ ] User: Cmd+Q → reopen; test success criteria with tab-containers on/off
