# Manual test plan — gvr-zen-mods ship stack

**Type:** manual · **Scope:** CSS rail UX (Zen Mods + expand-on-hover fork) · **Status:** living document

Versions come from each mod’s `manifest.json` at test time. Re-run after any change to `chrome.css`, install order, or expand-on-hover.

---

## Environment

| Item | Requirement |
|------|-------------|
| Browser | Zen Browser (vertical sidebar) |
| Profile | From `profiles.ini` default install; `ZEN_PROFILE=…` or `ZEN_PROFILE_PATH=…` to override |
| expand-on-hover | [GVR fork](https://github.com/froggabriel/zen-sidebar-expand-on-hover) · **v1.0.12-gvr** — `python3 install.py` in that repo, **before** mods here |
| Install order | eoh (external) → pinned-in-rail → pin-align → essentials-bottom → tab-containers → **rail-selected-ring last** |
| Restart | **Cmd+Q** quit, reopen — reload is not enough after `install.py` |

```bash
cd ~/Repos/zen-sidebar-expand-on-hover && python3 install.py
cd ~/Repos/gvr-zen-mods
python3 install.py pinned-in-rail pin-align essentials-bottom tab-containers rail-selected-ring
```

### Test data (minimum)

Prepare before regression runs:

- **Normal tabs:** at least one with a container identity (colored stripe).
- **Top-level pinned tab** (e.g. ProtonMail) — not in a folder.
- **Pinned tab inside `zen-folder`** (e.g. Gmail in E-mail folder) — reproduces historical #1 narrow-hover bug.
- **Drifted pinned tab** (`zen-pinned-changed`, slash reset control visible when expanded).
- **Essentials** row at bottom (YouTube/Gemini) — native tile grid; **not** in scope for rail bugs.
- **Nested folder** in pinned section (e.g. Banking → Banca) — folder indent scoping.

### Judging collapsed vs expanded

- **Collapsed steady state:** mouse **off** the sidebar; wait ≥ `--transition-delay-fast` (~500ms) after unhover before scoring.
- **Expanded:** hover sidebar (or open urlbar — expand-on-hover treats that as expanded).
- **Do not** score mid-transition unless the case explicitly says “during collapse”.

---

## Priority legend

| Priority | Meaning |
|----------|---------|
| **P0** | Ship blocker — stack unusable or major layout break |
| **P1** | Regression on shipped behavior — fix before merge/release |
| **P2** | Pref / edge case — verify when touching that mod |
| **P3** | Known open issue or optional mod |

---

## P0 — Smoke (every change)

| ID | Case | Steps | Expected |
|----|------|-------|----------|
| TC-SMOKE-01 | Install + load | Run install command; Cmd+Q; reopen Zen | No Mods errors; sidebar renders; all stack mods enabled in Zen Mods |
| TC-SMOKE-02 | Collapsed rail tiles | Mouse off sidebar; view workspace tabs | Square-ish tiles; container tabs show colored edge (stripe); icons centered |
| TC-SMOKE-03 | Sidebar expand | Hover sidebar | Full-width tab rows; labels visible; no favicon ghosts or `[` text bleed |
| TC-SMOKE-04 | Collapse snap | Unhover sidebar | Tabs snap to tile width immediately; labels hidden in rail (instant collapse) |
| TC-SMOKE-05 | Essentials position | Vertical sidebar | Essentials grid sits **below** workspace tabs, not overlapping scroll area |

---

## P1 — Ship stack regression

### Collapsed rail geometry (`tab-containers`)

| ID | Case | Steps | Expected |
|----|------|-------|----------|
| TC-TC-01 | Normal tab tile | Collapsed steady; normal container tab | Tile bg + stripe; icon centered in tile |
| TC-TC-02 | Top-level pinned tile | Collapsed steady; top-level pinned tab | Capped tile; icon centered; colored edge visible |
| TC-TC-03 | Pinned folder hover (#1) | Expand sidebar; hover pinned **folder** tab row (e.g. Gmail) | Full-width row, not half-width square |
| TC-TC-04 | Pinned folder collapsed | `zen-workspace[collapsedpinnedtabs]`; hover sidebar; folder pinned tabs | Flat rows (no extra folder indent); icons align with top-level pins |
| TC-TC-05 | Normal folder indent | Expanded sidebar; tab inside **normal-section** folder | Indented row; bg width follows indent |
| TC-TC-06 | Drifted pin icon | Collapsed steady; pinned tab with changed URL (`zen-pinned-changed`) | Favicon **centered** in tile; slash reset button **hidden** in rail |
| TC-TC-07 | Drifted pin expanded | Expand sidebar; same tab | Reset pin control visible again; row layout normal |

### Selection + tint (`rail-selected-ring`)

Default prefs: tile tint on; cap edges on; `hover_match_style` **off**.

| ID | Case | Steps | Expected |
|----|------|-------|----------|
| TC-RSR-01 | Selected container | Collapsed; select container tab | Selected tile tint; cap ring on 3 edges; **native stripe** remains 4th edge (left sidebar) |
| TC-RSR-02 | Selected non-container | Collapsed; select non-container tab | Neutral cap ring on top/bottom/sides; square tile geometry |
| TC-RSR-03 | Unselected tint | Collapsed; unselected tabs | Subtle tile background (if `tile_tint` on) |
| TC-RSR-03b | Tab hover tint | Collapsed; `hover_match_style` **off**; hover one unselected tab | Brighter `--rail-tile-hover-bg` on hovered tab only; neighbors keep idle tint |
| TC-RSR-04 | Expand clears ring | Select tab; hover sidebar to expand | Cap pseudo-elements and rail tint **cleared** — Zen native expanded tab chrome |
| TC-RSR-05 | Collapse restores ring | Unhover back to rail; same tab still selected | Caps + tint return without needing to re-select |

### Companions

| ID | Case | Mod | Steps | Expected |
|----|------|-----|-------|----------|
| TC-PIN-01 | Collapsed pins visible | pinned-in-rail | Workspace with `collapsedpinnedtabs`; collapsed rail | Loaded pins visible; pending tabs hidden; folder labels hidden |
| TC-PIN-02 | Pin folder alignment | pin-align | `collapsedpinnedtabs`; collapsed rail | Folder pinned icons align with top-level pins (no horizontal shift) |
| TC-EOH-01 | Hold clock present | expand-on-hover | Unhover sidebar from expanded | Normal tabs: brief label/icon hold before snap (eoh clock); then TC-SMOKE-04 snap |

---

## P1 — Accepted behavior (not bugs)

Document so future testers do not “fix” these again.

| ID | Behavior | Notes |
|----|----------|-------|
| TC-ACC-01 | Pinned **stripe snaps** on unhover | **#2 accepted** (v1.0.51+). Immediate pinned bg cap trades stripe hold for steady edge. |
| TC-ACC-02 | Essentials tile grid | Native Zen layout at bottom; side-by-side squares are correct. |
| TC-ACC-03 | First paint | Occasional one-frame flash on cold start — note in report; not a blocker unless reproducible every launch. |

---

## P2 — `rail-selected-ring` preferences

Re-run **TC-RSR-01..03** and **TC-RSR-04** under each row where relevant.

| ID | Pref | Setup | Expected |
|----|------|-------|----------|
| TC-RSR-P01 | `hover_match_style` **on** | Enable in Mods prefs; reinstall if needed | Collapsed: same as default. Expanded sidebar hover: **caps/tint stay** (TC-RSR-04 inverted). Tab hover in rail uses **idle** tint, not brighter hover wash. |
| TC-RSR-P02 | `tile_tint` **off** | Disable tint | Transparent tile bg; caps still work |
| TC-RSR-P03 | `tile_container_color` **on** | Container tabs only | Tint derived from identity color |
| TC-RSR-P04 | `cap_*` off (one edge) | Disable e.g. `cap_right` on left sidebar | Selected container: painted cap replaces native stripe on that edge; no double stripe |
| TC-RSR-P05 | `cap_unsel_*` on | Enable unselected caps | Unselected container/non-container caps render; native stripe hidden when caps conflict (see mod prefs) |

---

## P2 — Multi-workspace / sidebar edge

| ID | Case | Steps | Expected |
|----|------|-------|----------|
| TC-EDGE-01 | Right-side sidebar | Move sidebar right (`zen-right-side`); repeat TC-RSR-01 | Cap/stripe geometry mirrored; container stripe on correct edge |
| TC-EDGE-02 | Urlbar open | Collapsed rail; focus urlbar | Treated as expanded — rail caps cleared (default prefs) |
| TC-EDGE-03 | Popup open | Open tab context menu | Expanded styling path; no stuck collapsed caps |

---

## P3 — Known open / optional

| ID | Case | Status |
|----|------|--------|
| TC-OPEN-01 | Folder rename + mouse leaves sidebar | Sidebar collapses while folder name input focused — **unfixed** (eoh/upstream) |
| TC-OPT-01 | `active-first` | Optional mod — inactive tabs hidden in rail when pref on |

---

## Failure reporting

When a case fails, capture:

1. **Test ID** (e.g. `TC-TC-03`)
2. **Mod versions** (`manifest.json` for each mod in stack + eoh fork version)
3. **Workspace state** (expanded vs `collapsedpinnedtabs`, folder depth)
4. **Screenshot** — collapsed steady **and** expanded if transition bug
5. **Optional:** Browser Toolbox → inspect `tab .tab-background` computed `width`, `background-image`, `clip-path`

Golden visual references (pre-squash history tags on `main-pre-squash-20260620`): `golden-static`, `tc-baseline-v46`, `ship`.

---

## Future automation (out of scope for now)

Manual plan above maps cleanly to later layers:

| Layer | Candidate |
|-------|-----------|
| Install smoke | Script: `install.py` exit 0 + `zen-themes.css` contains mod IDs in order |
| CSS static | Assert no duplicate `@keyframes` removed hold anims; manifest version bumps match file headers |
| Browser | Playwright/Marionette against Zen profile — high cost; only for P0 smoke once stable selectors exist |
| Visual | Snapshot collapsed rail per theme — flaky; use only for tc-geometry with tight crop |

Until then, run **P0 + P1** before merge; **P2** when touching `rail-selected-ring` prefs or sidebar edge code.
