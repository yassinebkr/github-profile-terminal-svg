# Engineering OS — native README proof of concept

## Tested interaction
The GitHub renderer turns embedded SVGs into links to the underlying SVG file.
An image placed in the `<summary>` of a `<details>` therefore opens the SVG
when clicked, while the tiny native disclosure marker still expands the section.
This was reproduced by the user in GitHub's rendered README.

## Visual revision
- Retains a single Debian 13/XFCE terminal illustration at the top.
- Removes the fake input line on the illustration and the redundant [run] labels.
- Native `<summary><samp>...</samp></summary>` labels make each command clickable.
- Removes the grey `<code>` pills and distinct borders around the stdout images.
- Adds full software and fabrication modules.
- Keeps the SVG content in separate, readable, deterministic assets.

## Remaining hard limitations
The README simulates shell exploration through native disclosure elements.
Each disclosure manages its own expanded state, while SVG panels display
predetermined output. GitHub controls disclosure arrow styling. Clicking an
output SVG opens that asset in the GitHub file viewer.

## How to generate and validate
```bash
python3 scripts/make_terminal.py
python3 scripts/validate.py
```

## Manual check after each revision
1. Use GitHub's Preview tab for the README on this branch.
2. Click each **command text label** to expand its panel.
3. Check that hardware/embedded/software/fabrication and CinemaPi5/LoRa expand.
4. Confirm absence of extra `[run]` labels and grey code pills.
5. Check mobile width and GitHub light/dark themes.
6. If the browser image cache is stale, hard-refresh the README.
