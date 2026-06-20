# clean-sidebar-header — Agent Notes

**Version:** 1.0.0 · **Status:** Working · **Independent of GVR rail stack**

## Goal

Hide `#sidebar-header` (extension sidebar title bar) for a cleaner look. Tested with Side View; applies to other extension sidebars.

## Mechanism

Single rule in `chrome.css`:

```css
#sidebar-header { display: none !important; }
```

Also ships `userChrome.css` that `@import`s `chrome.css` for manual userChrome setups — **install.py only copies `chrome.css`** into zen-themes.

## Dependency

None. Not related to `zen-sidebar-expand-on-hover`.

## Critical lessons

1. Targets **extension sidebar**, not Zen’s vertical tab sidebar (`#navigator-toolbox`).
2. Trivial mod — avoid scope creep.

## Verify

Open an extension sidebar (e.g. Side View) — no title bar chrome above content.
