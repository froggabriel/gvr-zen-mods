# Expanded Tab Alignment — Design Spec

**Status:** Approved · **Phase:** B (then C)  
**Date:** 2026-06-18  
**Baseline:** tab-containers v1.0.5 + expand-on-hover “Working hold”

## Problem

On sidebar hover expand, tab icons/titles stay at collapsed-rail positions (left of + New Tab, label slivers). Collapse **hold** works; alignment does not.

## Root cause

Rail layout animations (`eoh-rail-margin-*`, `tc-rail-content`, `tc-rail-icon-margin`) use `animation: forwards`. They run outside the collapsed gate. On expand, `animation: none` clears the animation but **forwards-filled** flex/padding/margin on `.tab-content` persists. tab-containers loads last and overrides expand-on-hover hover resets.

## Goal (Phase B)

Hover expand (and urlbar-open): tab rows match vanilla Zen / + New Tab indent. Collapse hold unchanged.

## Non-goals (Phase B)

- `#tabs-newtab-button` padding/centering
- `eoh-label-rail` opacity fade timing
- Collapsed rail margin calcs (−23px) unless B doesn’t improve A
- Container stripe colors (Phase C)

## Approach (recommended)

1. **expand-on-hover:** Scope `eoh-rail-margin-*` / `eoh-rail-icon-*` to collapsed gate only (mirror tab-containers `:not(:hover, …)`).
2. **tab-containers:** On expand selectors, unset only `tc-rail-content` / `tc-rail-icon-margin` forwards (padding, display, flex, width, icon margins) — **not** tab row margins (expand-on-hover owns `margin-inline: 0` on expand).

## Success criteria

1. Hover expand: full titles, aligned with + New Tab  
2. Collapse hold: titles stick through delay, then snap  
3. No wrapped / multi-line labels  
4. Pass with tab-containers on and off  

## Phase C (after B)

`[usercontextid]` tabs: tile geometry only in rail (`tc-rail-bg-context`) — preserve container theme borders/backgrounds on pinned tiles.

## Revert

If hold breaks or labels wrap: revert expand-on-hover fork only first; then tab-containers expand block.
