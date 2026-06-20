# tab-containers — Agent Notes

**Version:** 1.0.51 (ship) · **Status:** instant collapse snap · **#2 accepted** (no label hold)

## Context handoff (read this first — Jun 2026 session)

**Install:** `python3 install.py zen-sidebar-expand-on-hover tab-containers pinned-in-rail pin-align` → **Cmd+Q**, reopen. **tab-containers loads last** in `zen-themes.css` (wins cascade over eoh).

**Ship stack:**

| Mod | Version | Role |
|-----|---------|------|
| expand-on-hover | **v1.0.11-gvr** | Primary hold: toolbox clip delay, `eoh-label-rail`, `eoh-rail-inset-*`. Pinned section collapsed default, expands on sidebar hover. |
| tab-containers | **v1.0.51** | v1.0.46 layout + **instant collapse** (snap edge + hide labels; no hold) |
| pin-align | v1.0.3 | Pinned-folder offset when `collapsedpinnedtabs` |
| pinned-in-rail | v1.0.1 | Collapsed pinned section visibility |

### Fixed (v1.0.46 — keep in baseline)

| Issue | Fix (tc only unless noted) |
|-------|------------------------------|
| **#1 hover narrow** (folder + top-level pinned) | Folder `.tab-group-container` hover column + tab `width:100%`; folder hover `.tab-background` `-moz-available` |
| **Label hold on unhover** (top-level e.g. ProtonMail) | `tc-rail-pinned-content` with `animation-fill-mode: both`: `from` = expanded row, `to` = capped centered icon |
| **Icon in tile after hold** | Same + icon-stack reset for all `tab[pinned]` (not just `zen-pinned-changed`) |

### #2 accepted — instant collapse (v1.0.51)

User accepts stripe snap. **v1.0.51** removes hold window: normal + pinned snap to tile on unhover; labels `display:none` immediately (overrides eoh `eoh-label-rail`). CSS-only stripe-hold attempts dead (v1.0.47–48, v1.0.50, eoh v1.0.12).

### Do not confuse with pinned

- **Essentials** (`tab[zen-essential]`, YouTube/Gemini at bottom): native tile grid, **no bugs**, out of scope.
- **Normal-section folder tabs** (E-mail/Banking when workspace expanded): separate indent behavior; not pinned #1/#2.

### Zen Mods philosophy (official — not our repo)

Per [Zen docs](https://docs.zen-browser.app/user-manual/extensions): **Zen Mods = CSS only** (browser UI). **Extensions = JS** (web content). Official loader (`ZenMods.mjs`) loads **`chrome.css`** only. **`rail-pending.uc.js`** is fx-autoconfig — outside Zen Mods model; eoh already has `[data-rail-pending="true"]` CSS hooks but nothing sets the attr without JS.

**User preference:** stay CSS-only for #2 (aligned with Zen Mods). JS is last-resort via autoconfig, not theme-store path.

### Next attempts (one mod, one log row)

| Priority | Mod | Hypothesis |
|----------|-----|------------|
| **1** | ~~**eoh only**~~ | **Dead:** v1.0.12-gvr — #2 unchanged both modes; **regression:** folder pinned icons shifted right when workspace expanded. Reverted to v1.0.11-gvr. |
| **2** | ~~**tc scoped cap**~~ | **Dead:** v1.0.50 — **split by workspace mode.** `[collapsedpinnedtabs]` = v1.0.49 (edge ✓, snap ✗). Expanded = **no steady edge**, unhover **narrow tabs shifted right**. Reverted to v1.0.49. |
| **3** | **paired (JS)** | `rail-pending.uc.js` + tc cap `:not([data-rail-pending])` — only remaining path if #2 matters; eoh hooks exist (~728–730). Off Zen Mods model. |

**Do not bundle (kills baseline):** eoh always-expanded pinned section + tc hold; instant pinned label hide; tc instant section width override.

**Do not touch when fixing #2:** `tc-rail-pinned-content`, `tc-rail-hide-label`, folder hover column rules (v1.0.46).

**Transcript:** `agent-transcripts/58fc4eed-fbe8-43e1-be00-717303da1221.jsonl` · **DOM dump:** `pinned-gmail-tab.txt` (lines 1–49 useful; rest is accidental toolbox dump)

---

**Maintained from user input + transcript.** When testing a stack, add a row: both mod versions, what changed in each, your feedback. Transcript archive: `agent-transcripts/58fc4eed-fbe8-43e1-be00-717303da1221.jsonl`.

**Current installed baseline:** tab-containers **v1.0.49** + expand-on-hover **v1.0.11-gvr** (+ pin-align v1.0.3, pinned-in-rail v1.0.1).

### Golden references (user-confirmed)

| Ref | What user said |
|-----|----------------|
| **`4fd2ba0` / tc v1.0.5 static CSS** | “Beautiful” collapsed + expanded; square tiles + stripes. **Does not hold** on unhover. |
| **`435b945` / tc hold animations** | “First working hold” for normal tabs. Must **layer on** static CSS, not replace it. |
| **`1688c30` / eoh hold** | “Working hold” — primary hold clock (`eoh-label-rail`, `eoh-rail-inset-*`, toolbox clip delay). |
| **tc v1.0.46 + eoh v1.0.11-gvr** | **Ship baseline** (v1.0.49): hover rows ✓, label/icon hold ✓, steady edge ✓; stripe snap open (#2) |

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
| **v1.0.45** | Folder `.tab-group-container` hover column + tab 100%; `tc-rail-pinned-content` (content width = bg cap); icon-stack reset all `[pinned]` | **v1.0.11-gvr** | (unchanged) | Top-level pinned OK; icon aligned on unhover ✓; **label hold lost** ✗; folder Gmail hover still narrow; stripe snap unchanged; normal tabs unchanged. |
| **v1.0.46** | `tc-rail-pinned-content` `both` + from=expanded row / to=capped icon; folder pinned hover `.tab-background` `-moz-available` | **v1.0.11-gvr** | (unchanged) | **Confirmed**: ProtonMail label hold ✓, icon centered in tile ✓; folder Gmail hover full rows ✓; stripe snap unchanged ✗. **New baseline** for pinned layout/hold. |
| **v1.0.47** | Delay pinned `.tab-background` cap via `tc-rail-pinned-bg-cap` (same end width); split bg-color anims for pinned vs normal | **v1.0.11-gvr** | (unchanged) | **Partial #2**: stripe hold ✓ when workspace pins **collapsed**; hold ✗ when workspace+folders **expanded**. Steady collapsed rail: square tile ✓, **no colored edge** ✗ (regression vs v1.0.46). Hover + label/icon hold ✓. First load improved (label ~2s then cap+color, no hover cycle needed). |
| **v1.0.48** | `tc-rail-pinned-bg-cap` add `from` (-moz-available) + `both` fill so cap restarts on each unhover | **v1.0.11-gvr** | (unchanged) | **No change vs v1.0.47** (user confirmed). Reverted with v1.0.49. |
| **v1.0.49** | Revert v1.0.47/48 delayed pinned bg cap; restore immediate static cap | **v1.0.11-gvr** | (unchanged) | Restore v1.0.46 steady colored edge + layout/hold; stripe snap unchanged. **Ship baseline.** |
| **eoh v1.0.12-gvr** | Skip folder `translateX`/padding indent in pinned section when `zen-workspace:not([collapsedpinnedtabs])` on sidebar unhover | **tc v1.0.49** | (unchanged) | **Dead end.** #2 snaps both modes. Workspace expanded: folder pinned icons **shifted right** (regression). Reverted eoh to v1.0.11-gvr. |
| **tc v1.0.51** | Replace hold animations with instant collapsed static rules; labels `display:none` + override eoh label fade | **eoh v1.0.11-gvr** | (unchanged) | User choice: accept snap; no edge-then-text on unhover. *(pending test)* |

### Pinned-specific feedback (by state)

| State | Good (baseline) | Bad (what triggered revert) |
|-------|-----------------|------------------------------|
| **Collapsed steady** | Square tile + colored edge | No edge; wide pill; `[` text bleed |
| **Expanded hover** | Full-width rows + labels | ~~Half-width squares~~ fixed v1.0.46 |
| **Unhover hold** | Normal + pinned: title holds ~500ms; pinned icon centered in tile (v1.0.46) | Pinned **stripe/edge** snaps (#2); v1.0.45 label hold regression (fixed v1.0.46) |
| **First load** | v1.0.49 steady edge OK | v1.0.47: label ~2s then cap+color without hover cycle (interesting; lost on revert) |

### Bundled failures (both mods — don’t ship in one diff)

| tab-containers + expand-on-hover bundle | User result |
|----------------------------------------|-------------|
| tc pinned hold anims + eoh section always expanded | Collapsed edge lost |
| tc instant pinned label hide + any hold | Unhover loses label hold |
| tc instant center + eoh always-expanded section | Collapsed rail empty |
| tc instant section width + eoh width transition | Unhover hold killed (v1.0.40) |
| tc `:not([pinned])` + eoh `:not([pinned])` insets (v1.0.42) | No visible change |
| tc pinned content reset + eoh folder scope (v1.0.43) | Left shift + text bleed |

### Open problem (#2 — stripe hold)

Pinned stripe snap vs tc **immediate** pinned bg cap. Labels hold via `tc-rail-pinned-content` + `eoh-label-rail` — **do not touch those** when fixing stripe.

**tc global cap delay:** tried v1.0.47–48, scoped v1.0.50 — all reverted. **CSS-only #2 exhausted** unless user wants `rail-pending.uc.js`.

~~**Next isolated experiments (one mod, one row in log):**~~ → see **Context handoff** table above.

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

**Rule for next agent:** v1.0.46+ pinned layout/hold is **shipped** — do not regress. For #2: prefer **eoh-only** row first (workspace-expanded unhover). tc cap changes load **last** and beat eoh — pairing requires tc to **gate** cap, not eoh to override cap.

**Pinned cap conflict (confirmed v1.0.50):** immediate cap ↔ stripe hold is a **hard tradeoff**, split by `zen-workspace[collapsedpinnedtabs]`. Scoped delay fixes neither mode cleanly.

Conflict (historical): static `width !important` on tab applies immediately on unhover and **defeats** width hold. Options:

- A) Ship 4fd2ba0 only (no tab-containers hold; expand-on-hover hold from `1688c30` may be enough).
- B) Remove static width from 4fd2ba0; use `tc-rail-width` animation only; keep static `.tab-background` + add `!important` in keyframe `to` if needed for width.
- C) `data-rail-pending` + `rail-pending.uc.js` — **off-model for Zen Mods**; user prefers CSS. eoh CSS hooks exist at `chrome.css` ~728–730.

## v1.0.46 shipped CSS (do not regress)

- Folder pinned hover: `zen-folder .tab-group-container` column + tab `width:100%` + `.tab-background` `-moz-available`
- Pinned unhover content: `tc-rail-pinned-content` (`both`, from expanded row → to capped icon)
- Icon-stack reset: all `tab[pinned]` in pinned section on `:not(:hover)`
- Immediate pinned bg cap (v1.0.49): static width on pinned `.tab-background` for steady colored edge

## Companion mods at golden visual baseline

At `4fd2ba0` / current v1.0.8:

- **pinned-in-rail** v1.0.1 (no Case E folder width — added in v1.0.2 / `435b945` era)
- **pin-align** v1.0.2
- **expand-on-hover** v1.0.5-gvr (must include `1688c30` hold + container clip exemption)

Install order in `zen-themes.css`: expand-on-hover → pinned-in-rail → pin-align → **tab-containers last**.

## Optional JS hold (off-model)

`rail-pending.uc.js` sets `data-rail-pending="true"` during collapse delay. eoh reacts (`animation: none` on labels, full `.tab-background` clip). `install.py` copies only if `chrome/utils/` exists (fx-autoconfig). **Not Zen Mods path** — see Context handoff.

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
