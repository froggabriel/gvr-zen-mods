# Experiment B′ — Expanded Alignment (minimal)

**Status:** Active  
**Baseline:** Working hold (`1688c30` expand-on-hover, tab-containers v1.0.5)

## Change

1688c30 hold commit replaced instant rail margins with delayed `animation: forwards`, and added **`margin-left: 0 !important`** on expand — that zeroes Zen indent while forwards can still stick.

Fix (keep hold animations):
1. Collapsed gate: `eoh-label-rail`, `eoh-rail-margin-*`, folder `translateX(±14px)`
2. Expand: **`margin-inline: unset !important`** on `.tab-content` / icons (not `0`, not padding hacks) + `animation: none`

## Revert if

Hold breaks, labels wrap, or expanded looks worse than baseline.

## Not in B′

- tab-containers changes
- `#tabs-newtab-button` 
- folder indent scoping
- `margin-inline: 0` / `display: unset` on expand
