# tab-containers — Agent Notes

**Version:** 1.0.5 · **Status:** collapse hold via CSS animation (known-good baseline)

## Collapse hold

Full rail snap delayed via `animation` + `--transition-delay-fast`. No `display: none` on labels — expand-on-hover `eoh-label-rail` fades them after the same delay.

Optional: `rail-pending.uc.js` + fx-autoconfig (`data-rail-pending` gate).

## Install

```bash
python3 install.py tab-containers zen-sidebar-expand-on-hover
```

Quit Zen (Cmd+Q) before testing. Re-enable mod in Zen settings after A/B toggles, then reinstall if needed.

## Known follow-ups (not in this commit)

- Icon alignment in steady collapsed rail
- Instant `!important` tile backgrounds if animation `forwards` stops persisting in a Zen update
