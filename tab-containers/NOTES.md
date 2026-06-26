# tab-containers — Agent Notes

**Version:** 1.0.58 · **Status:** ship · **#2 accepted** (instant collapse, stripe snap OK)

## Install stack (order matters)

```bash
python3 install.py pinned-in-rail pin-align essentials-bottom tab-containers rail-selected-ring
```

Cmd+Q, reopen. **tab-containers** loads before **rail-selected-ring** (last wins on tile tint/selection).

| Mod | Version | Role |
|-----|---------|------|
| expand-on-hover | [GVR fork](https://github.com/froggabriel/zen-sidebar-expand-on-hover) v1.0.12-gvr | **External** — install first (`python3 install.py` in that repo); primary hold clock, pinned section collapsed default |
| pinned-in-rail | v1.0.1 | Pinned tabs visible when workspace section collapsed |
| pin-align | v1.0.4 | Folder-tab icon alignment in collapsed pins |
| essentials-bottom | v1.0.8 | Essentials under workspace tabs |
| tab-containers | **v1.0.58** | Tile geometry, folder indent, instant collapse |
| rail-selected-ring | v1.3.3 | Collapsed-rail tile tint + selected cap ring |

`active-first` and `clean-sidebar-header` are optional; not in the ship stack.

## Golden refs (git tags on `main-pre-squash-20260620`)

| Tag | Commit | Meaning |
|-----|--------|---------|
| `golden-static` | `4fd2ba0` | Beautiful static collapsed tiles + native stripes |
| `golden-hold-sync` | `435b945` | First working tc hold sync layer (on top of static) |
| `tc-baseline-v46` | `7bc0c42` | Pinned layout/hold baseline (#1 fixed) |
| `tc-instant-collapse` | `1c7328b` | User accepted stripe snap; hold removed |
| `ship` | `014511a` | Pre-squash tip (same tree as current) |

Full iteration log lives in pre-squash history — do not replay dead ends here.

## Shipped behavior (do not regress)

**v1.0.46 pinned layout** (still in v1.0.58):

- Folder pinned hover: `zen-folder .tab-group-container` column + tab `width:100%` + `.tab-background` `-moz-available`
- Pinned collapsed: icon-stack reset for all `tab[pinned]`; immediate pinned `.tab-background` cap
- **v1.0.51+:** instant collapse — labels `display:none` on unhover (no hold window); user accepts stripe snap

**v1.0.68:** drop speaker pill bg (stripe conflict already handled via `.tab-context-line` hide).

**v1.0.67:** scope audio overlay to `[soundplaying]` only — fixes ghost squares on idle tabs.

**v1.0.65:** collapsed rail audio — default `display:none` on `.tab-audio-button` (eoh only `opacity:0`, still shifts favicon); pref `mod.gvr-tab-containers.show_audio_in_rail` for top-right speaker overlay above rail-selected-ring stripes.

**v1.0.58:** folder indent scoped by section (`normal` vs `pinned:not([collapsedpinnedtabs])`); hide `.tab-reset-pin-button` in collapsed rail (drifted-pin favicon shift).

## #1 root cause (folder hover narrow)

Hover flex for folder pinned tabs lives in **`zen-folder .tab-group-container`** (row, ~119px), not the outer pinned vbox. Fix: column + `width:100%` on container and tabs.

**Essentials** (`tab[zen-essential]`) are out of scope — native tile grid at bottom.

## Stripes

Native `.tab-context-line` on `.tab-background`. tab-containers does not paint stripes. Requires static collapsed rules:

- `tab { width: calc(var(--collapsed-tab-bar-width) - 5px) !important; }`
- `.tab-background { clip-path: none !important; width: -moz-available; … }`
- expand-on-hover container clip exemption (non-container tabs only)

**#2 tradeoff:** immediate pinned bg cap = steady edge ✓, stripe snaps on unhover ✗. Delayed cap attempts (v1.0.47–48, v1.0.50) and eoh v1.0.12 reverted. CSS-only #2 exhausted; instant collapse shipped.

## Hold architecture

Most hold is **expand-on-hover** (`1688c30` / tag on eoh repo). tab-containers **435b945** was a sync layer (`tc-rail-*` on same clock). **v1.0.51** removed tc hold — instant static collapse only.

Do not bundle: eoh always-expanded pinned section + tc hold; instant pinned label hide + any hold; tc instant section width override.

## What kills stripes (don't repeat)

- Animation-only `.tab-background` without static `!important` rules
- Gating static bg with `[data-rail-pending="true"]`
- `background:` shorthand in hold keyframes
- `margin-inline: auto` on tabs; synthetic `::after` / box-shadow stripe hacks
- pinned-in-rail Case E `width:100%` on folder container tabs (fights tile width)

## Known follow-ups

- Folder rename + sidebar collapse while input focused (eoh / upstream)
- Pinned Gmail in `zen-folder` + `collapsedpinnedtabs` — pinned-in-rail Case E may return; exclude container tabs from width overrides
