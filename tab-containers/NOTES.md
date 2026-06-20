# tab-containers — Agent Notes

**Version:** 1.0.25 (confirmed baseline) · **Status:** OK except pinned hover narrow + pinned stripe snap on unhover

## Context handoff (read this first)

**Install:** `python3 install.py zen-sidebar-expand-on-hover tab-containers pinned-in-rail pin-align` → **Cmd+Q** Zen, reopen. tab-containers loads **last** in `zen-themes.css`.

**Stack (Jun 2026 baseline):**

| Mod | Version | Role |
|-----|---------|------|
| expand-on-hover | **v1.0.11-gvr** | Primary hold: toolbox clip delay, `eoh-label-rail`, `eoh-rail-inset-*`. Pinned section collapsed default, expanded on hover. Folder width `expanded - 28px` hover-only (v1.0.9). |
| tab-containers | **v1.0.25** | Static tile geometry + immediate pinned bg cap. Companion hold: `tc-rail-width` / content / labels (same `--transition-delay-fast` clock). |
| pin-align | **v1.0.3** | Pinned-folder `-14px` reset when `collapsedpinnedtabs` (no dead `@media`). |
| pinned-in-rail | **v1.0.1** | Collapsed pinned section visibility (no Case E folder width). |

**Works on baseline (user-verified):**
- Normal tabs: collapsed stripes/tiles, expanded hover, **unhover hold** (title + stripe ~500ms)
- Pinned tabs: collapsed steady — square tile + **colored edge**; **label hold on unhover matches normal** (fade/hold OK)

**Only two open bugs (`[pinned]` in pinned section — not Essentials):**
1. **Hover narrow** — pinned tabs are side-by-side half-width squares, not full-width rows with labels
2. **Unhover stripe snap** — pinned **colored edge** snaps immediately; labels still hold. Normal stripe holds through delay

**Out of scope (no bugs):** Bottom **Essentials** (`tab[zen-essential]`, e.g. YouTube, Gemini) — native Zen tile grid; tab-containers explicitly excludes `[zen-essential]`. Side-by-side square tiles there are correct.

### Inspection findings (`pinned-gmail-tab.txt`, Jun 2026)

Gmail pinned tab path: `…pinned-tabs-section → zen-folder → .tab-group-container → tab[pinned]` (folder pinned tab, not top-level).

| Layer | display / flex | width | Notes |
|-------|----------------|-------|-------|
| `tab` | flex **row** | **40px** | collapsed tile width at capture |
| `.tab-group-container` | block **row** | **119px** | **Likely #1 culprit** — row container inside folder; v1.0.44 column on outer vbox never reaches here |
| `zen-folder` | flex column | 136px | |
| pinned section vbox | flex **column** | 148px | already column — explains v1.0.44 no change |

**tab-background computed (unhover):** pinned static cap wins — `calc(collapsed - 5px - 2*margin)` beats `-moz-available` static + Zen native. Confirms bug #2: stripe follows `.tab-background` cap, not label hold.

**User note:** `.tab-stack` drives label width; `.tab-background` drives colored edge width — explains label hold vs stripe snap split.

**Next #1 target:** hover `flex-direction: column` (+ full width) on `vbox…pinned-tabs-section zen-folder .tab-group-container`, not outer pinned vbox.

**Constraints:** CSS-only for pinned stripe hold (no `data-rail-pending` / `rail-pending.uc.js` unless user changes mind). One change per attempt; log row in combined table below.

**Do not bundle (kills baseline):** eoh section always expanded + pinned hold; instant pinned label hide; instant pinned icon center; tc instant section width override.

**Next isolated tries (one at a time):**
- **tc only:** hover column + stretch on `pinned-tabs-section zen-folder .tab-group-container` (report: outer vbox already column; row flex is inside folder container)
- **tc only:** delay pinned `.tab-background` cap only — keep static cap end state; labels untouched (fix #2)

**Architecture reminder:** Hold is mostly **expand-on-hover** (`1688c30`). tab-containers syncs width/layout/tiles. Static `.tab-background` block (`clip-path: none !important`, `-moz-available`) must stay immediate — stripes are emergent, not painted by tc.

**Transcript:** `agent-transcripts/58fc4eed-fbe8-43e1-be00-717303da1221.jsonl`

---

**Maintained from user input + transcript.** When testing a stack, add a row: both mod versions, what changed in each, your feedback. Transcript archive: `agent-transcripts/58fc4eed-fbe8-43e1-be00-717303da1221.jsonl`.

**Current installed baseline:** tab-containers **v1.0.25** + expand-on-hover **v1.0.11-gvr** (+ pin-align v1.0.3, pinned-in-rail v1.0.1).

### Golden references (user-confirmed)

| Ref | What user said |
|-----|----------------|
| **`4fd2ba0` / tc v1.0.5 static CSS** | “Beautiful” collapsed + expanded; square tiles + stripes. **Does not hold** on unhover. |
| **`435b945` / tc hold animations** | “First working hold” for normal tabs. Must **layer on** static CSS, not replace it. |
| **`1688c30` / eoh hold** | “Working hold” — primary hold clock (`eoh-label-rail`, `eoh-rail-inset-*`, toolbox clip delay). |
| **tc v1.0.25 + eoh v1.0.11-gvr** | Baseline: collapsed edge ✓, label hold ✓ (pinned labels match normal); **open:** hover narrow, pinned **stripe** snap on unhover |

### Combined stack log

| tc | tab-containers change | eoh | expand-on-hover change | User feedback |
|----|----------------------|-----|------------------------|---------------|
| **v1.0.5** | Static tile bg + immediate collapsed width | *(fork 1688c30 hold)* | Clip-path rail; container clip exemption TBD | “Fantastic” / “beautiful” — revert target |
| **v1.0.6–9** | Split pinned/unpinned, transitions, flex-center | — | — | “No change since 1.0.8” — invisible in Zen |
| **v1.0.10** | Remove label `display:none`; delay via `--transition-delay-fast` | — | — | Snap instantly; pinned left, normal slightly left (balanced) |
| **v1.0.11+** | Keyframes without `!important` on animated props | — | — | Still “back to 1.0.5 behavior” |
| **v1.0.12** | Collapsed rail overhaul (stripes, tiles) | — | — | Normal collapsed+expanded broken; pinned text bleed |
| **v1.0.19–20** | Box-shadow / native stripe experiments | **v1.0.5-gvr** | Container tabs exempt from collapsed bg clip-path | v1.0.19: weird unhover stripes; v1.0.20: step toward fix |
| **v1.0.22–24** | `::after` stripe; hover `width:100%`; context-line restore | — | — | “No visible change” on stripes |
| **v1.0.25** | Immediate static pinned bg cap; stripe from static tile | **v1.0.5-gvr+** | Container clip exemption (paired with tc) | **Baseline**: edge ✓, label hold ✓; hover narrow + pinned snap |
| **v1.0.26** | Hover flex column; `tc-rail-pinned-width` + delayed bg cap | **v1.0.11-gvr** | Pinned section collapsed default / expand on hover | Hold ✗; text bleed; narrow hover |
| **v1.0.27** | Instant pinned label hide; column; pinned content hold | **v1.0.12-gvr** | Pinned section **always expanded** width | **Rejected**: no collapsed edge; unhover loses label |
| **v1.0.36** | Removed instant pinned bg cap; pinned hold anims | **v1.0.8-gvr** | Pinned section collapsed default; width transition on hold clock | Steady collapsed stripes OK; unhover hold attempt |
| **v1.0.38** | Revert v1.0.37; restore instant static pinned cap | **v1.0.10-gvr** | Pinned section **always expanded** (revert v1.0.8) | — |
| **v1.0.39** | `tc-rail-pinned-width` both fill + delayed bg cap | **v1.0.10-gvr** | Always expanded pinned section | Unhover OK; hover narrow; collapsed missing edge |
| **v1.0.40** | Instant collapsed section width + hover column | **v1.0.11-gvr** | Collapsed pinned section + expand on hover | Bad: killed unhover hold |
| **v1.0.41** | Column + center on collapsed; removed tc section width | **v1.0.11-gvr** | (same) | Ghosts, lost icons, centered icons on unhover |
| **v1.0.42** | `:not([pinned])` scoping; hover column only | **v1.0.11-gvr** | `:not([pinned])` on eoh rail insets | “No visible change” |
| **v1.0.43** | Folder scope normal-section; pinned content resets | **v1.0.11-gvr** | Normal-section folder transform only | **Worse**: shifted left, text bleed |
| **v1.0.25** *(restore)* | Revert to v1.0.25 | **v1.0.11-gvr** | Collapsed default + hover expand | **Confirmed baseline** — hover narrow; pinned **stripe** snaps on unhover; labels hold |

*Rows after v1.0.25 restore: add new attempts below this line.*

| tc | tab-containers change | eoh | expand-on-hover change | User feedback |
|----|----------------------|-----|------------------------|---------------|
| **v1.0.44** | Hover `flex-direction: column` on pinned section only | **v1.0.11-gvr** | (unchanged) | **No change vs v1.0.25 baseline** (user confirmed no regression). Baseline detail: nested folder tabs (Banking) same width but indented right on hover; unhover shift + stripe snap unchanged. Essentials (YouTube/Gemini) are not pinned — ignore for #1. Reverted. |

### Pinned-specific feedback (by state)

| State | Good (baseline) | Bad (what triggered revert) |
|-------|-----------------|------------------------------|
| **Collapsed steady** | Square tile + colored edge | No edge; wide pill; `[` text bleed |
| **Expanded hover** | Full-width rows + labels | Half-width squares; tabs too short |
| **Unhover hold** | Normal + pinned: title holds ~500ms | Pinned **stripe/edge** snaps (labels OK); centered icon → empty clip if mis-fixed |
| **First load** | — | Text bleed until first hover/unhover |

### Bundled failures (both mods — don’t ship in one diff)

| tab-containers + expand-on-hover bundle | User result |
|----------------------------------------|-------------|
| tc pinned hold anims + eoh section always expanded | Collapsed edge lost |
| tc instant pinned label hide + any hold | Unhover loses label hold |
| tc instant center + eoh always-expanded section | Collapsed rail empty |
| tc instant section width + eoh width transition | Unhover hold killed (v1.0.40) |
| tc `:not([pinned])` + eoh `:not([pinned])` insets (v1.0.42) | No visible change |
| tc pinned content reset + eoh folder scope (v1.0.43) | Left shift + text bleed |

### Open problem (CSS-only)

Pinned **stripe hold on unhover** vs **immediate static pinned bg cap** (v1.0.25 steady collapsed edge). Labels already hold — do not touch label rules when fixing stripe. User prefers **no JS**.

**Next isolated experiments (one mod, one row in log):**
- **tc only:** hover `flex-direction: column` on pinned section → fix hover narrow
- **tc only:** delay pinned bg cap only (same end cap as v1.0.25 static); do not delay labels
- **eoh only:** *(none queued — baseline v1.0.11-gvr)*

---

## Golden commits (do not conflate)

| What | Repo | Commit | Notes |
|------|------|--------|-------|
| **Collapsed + expanded visuals (stripes, square tiles)** | `gvr-zen-mods` | `4fd2ba0` | `tab-containers` v1.0.5 static CSS. User-confirmed “beautiful” rail. **No stripe-specific rules** — stripes are emergent. |
| **Collapse hold (primary)** | `zen-sidebar-expand-on-hover` | `1688c30` | “Working hold”. `eoh-label-rail`, `eoh-rail-inset-*`, `data-rail-pending` on `#navigator-toolbox`, delayed margin/icon animations. Paired in time with `435b945`. |
| **Collapse hold (companion)** | `gvr-zen-mods` | `435b945` | `tc-rail-width` / `tc-rail-bg` / `tc-rail-content` / `tc-rail-hide-chrome` animations on same `--transition-delay-fast` clock. **Does not replace** 4fd2ba0 static `.tab-background` rules. |

**Wrong assumption we kept repeating:** hold lives only in tab-containers. Most hold is **expand-on-hover** (`1688c30`). tab-containers hold is a **sync layer** for tile width/layout — not the stripe layer.

## What makes collapsed stripes work (4fd2ba0)

Stripes are **native** `.tab-context-line` (orange/blue container color). tab-containers does not paint them. All of this must work together:

1. **tab-containers** — static, immediate on `:not(:hover)` (no `data-rail-pending` on these):
   - `tab { width: calc(var(--collapsed-tab-bar-width) - 5px) !important; }`
   - `.tab-background { clip-path: none !important; width: -moz-available; … }`
   - `.tab-content` centered; `.tab-label-container { display: none !important; }`
2. **expand-on-hover** — container tabs **exempt** from collapsed `.tab-background` clip-path sliver:
   - `tab:not([usercontextid]):not(:has(> .tab-stack > .tab-background > .tab-context-line)) .tab-background`
   - Without exemption, clip chops ~110px from the right where the stripe lives.
3. **Essentials** at bottom use native Zen tile sizing; workspace tabs match via tab-containers width + bg rules above.

User’s container theme (`cb5efa80`) sets `.tab-context-line { display: none !important }` globally. Stripes still showed at `4fd2ba0` — full tile + `clip-path: none` + trailing layout is enough for native line to paint in practice. Do not “fix” stripes with synthetic `box-shadow` / `::after` until static baseline is regressed.

## What kills stripes (failed experiments v1.0.7–1.0.27)

- Replacing **static** 4fd2ba0 rules with **animation-only** for `.tab-background` (keyframes without `!important` lose to expand-on-hover clip).
- Gating static `.tab-background` with `[data-rail-pending="true"]` — stripes disappear in steady collapsed.
- `background:` shorthand in `tc-rail-bg` keyframes — resets `background-image` / kills `::after` / box-shadow on same element.
- Animating width/content/labels **without** static collapsed width — tabs stay expanded width; toolbox clip shows icon + first letter (“D”, “N”), stripe off-screen to the right.
- `margin-inline: auto` on tabs — tiles leave the rail.
- `flex` / `::after` / `box-shadow` stripe hacks — flash on unhover, straight edges, fight container theme borders.
- **pinned-in-rail** Case E `width: 100% !important` on folder tabs — fights `tc-rail-width` (exclude container tabs if Case E returns).

## Hold architecture (target state)

```
expand-on-hover (1688c30)     tab-containers (435b945 companion)     4fd2ba0 static (keep)
─────────────────────────     ──────────────────────────────────     ─────────────────────
toolbox clip delay            tc-rail-width (tab width)              .tab-background clip-path:none !important
eoh-label-rail (opacity)      tc-rail-content / icon-margin          .tab-background backgrounds !important
eoh-rail-inset-* (padding)    tc-rail-hide-chrome (close btn)        .tab-content center + label display:none
data-rail-pending freeze      (optional rail-pending.uc.js)          pinned icon-stack reset
```

**Rule for next agent:** add hold by layering **435b945 animations on width/content/icons/labels only**. **Never animate or gate** the 4fd2ba0 `.tab-background` static block. Selectors for static bg stay:

`#navigator-toolbox:not(:hover, [has-popup-menu="true"], …)` — **no** `[data-rail-pending="true"]`.

Conflict: static `width !important` on tab applies immediately on unhover and **defeats** width hold. Options:

- A) Ship 4fd2ba0 only (no tab-containers hold; expand-on-hover hold from `1688c30` may be enough).
- B) Remove static width from 4fd2ba0; use `tc-rail-width` animation only; keep static `.tab-background` + add `!important` in keyframe `to` if needed for width.
- C) `data-rail-pending` + `rail-pending.uc.js` to suppress static width during hold window only.

Do **not** merge by replacing the whole file with animation-only 435b945 (loses `!important` on bg) or v1.0.6-style “static bg + animated width” with `data-rail-pending` on bg.

## Companion mods at golden visual baseline

At `4fd2ba0` / current v1.0.8:

- **pinned-in-rail** v1.0.1 (no Case E folder width — added in v1.0.2 / `435b945` era)
- **pin-align** v1.0.2
- **expand-on-hover** v1.0.5-gvr (must include `1688c30` hold + container clip exemption)

Install order in `zen-themes.css`: expand-on-hover → pinned-in-rail → pin-align → **tab-containers last**.

## Optional JS hold

`rail-pending.uc.js` sets `data-rail-pending="true"` on `#navigator-toolbox` during collapse delay. expand-on-hover already reacts (`animation: none` on labels, full tab-background clip on pending). `install.py` skips copy if profile has no `chrome/utils/` (fx-autoconfig). Release profile often needs manual setup.

## Install / test

```bash
python3 install.py zen-sidebar-expand-on-hover tab-containers pinned-in-rail pin-align
```

**Cmd+Q** quit Zen, reopen. Mouse off sidebar, wait past `--transition-delay-fast` (~500ms + duration) before judging collapsed steady state.

## Reference dumps (Browser Toolbox)

- `normal-tab-context-line-style.txt` / `pinned-tab-context-line-style.txt` — computed styles when stripes work (orange `rgb(255,159,0)`, 3px width).

## Pinned tab width (v1.0.14–1.0.17 learnings)

- **Never** a separate pinned-only `tab` width animation — excludes pinned from unified hold and breaks collapsed stripes.
- **Never** `!important` on `tc-rail-width` `@keyframes to` (even unified) — breaks **all** collapsed container stripes/edges (v1.0.16).
- **Expanded:** pinned section `vbox.zen-workspace-tabs-section.zen-workspace-pinned-tabs-section` gets same width/margin as `.workspace-arrowscrollbox`; tabs use `width: auto` like normal.
- **Expanded pinned width:** tab-containers v1.0.22+ — split `width:auto` (normal) vs `width:100%` (pinned section).
- **Expanded selected/hover bg:** v1.0.23 — `background-color: unset` on expand (not `background: revert`).
- **Pinned collapsed tile cap:** v1.0.18/25 immediate static `.tab-background` cap + `overflow:hidden`. **v1.0.23–24 reverted** — delayed cap / immediate label hide broke stripes and hold.
- **First-load bleed:** v1.0.30 — `max-width` + padding inset **without** `!important` on the property (transition on the rule only): immediate on cold start, delayed on unhover. All `[pinned]` icon-stack reset (was `zen-pinned-changed` only — caused first-load slivers). v1.0.27 `!important` max-width fixed cold start but killed hold.
- **Label hold on unhover:** v1.0.28 restored `tc-rail-hide-label` + expand-on-hover `eoh-label-rail`; v1.0.29 removes the tab `max-width` that made v1.0.28 look unchanged.
- **Pinned stripe hold on unhover:** v1.0.35 reverts v1.0.25 collapsed baseline (v1.0.31–34 experiments reverted). Pinned cap gated `:not([data-rail-pending])`; `rail-pending.uc.js` suppresses cap during hold (needs fx-autoconfig program/ in Zen.app). v1.0.34 `@container`/`--tc-hold-expanded` removed — style queries did not apply in Zen.

## v1.0.9 merge (2026-06)

- **Animated (435b945):** `tc-rail-width`, `tc-rail-content`, `tc-rail-icon-margin`, `tc-rail-hide-chrome` (close/reset only).
- **Static (4fd2ba0):** entire `.tab-background` block with `!important` — no `data-rail-pending` gate, no keyframes.
- **Removed from tab-containers:** `display: none` on `.tab-label-container` — expand-on-hover `eoh-label-rail` owns label fade during hold.

## Known follow-ups
- Folder rename focus + sidebar collapse (expand-on-hover / Zen upstream).
- Pinned Gmail in `zen-folder` + `collapsedpinnedtabs` — may need pinned-in-rail Case E again, but **exclude** `[usercontextid]` / container tabs from width overrides.
