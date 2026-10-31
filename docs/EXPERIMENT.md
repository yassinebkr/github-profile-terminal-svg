# Engineering OS — native README proof of concept

## Tested interaction
The GitHub renderer turns embedded SVGs into links to the underlying SVG file.
An image placed in the `<summary>` of a `<details>` therefore opens the SVG
when clicked, while the tiny native disclosure marker still expands the section.
This was reproduced by the user in GitHub's rendered README.

## Visual revision
- Retains a single Debian 13/XFCE terminal illustration at the top.
- Removes the fake input line on the illustration and the redundant [run] labels.
- Commands are native `<summary><samp>...</samp></summary>` text, not clickable images.
- Removes the grey `<code>` pills and distinct borders around the stdout images.
- Adds full software and fabrication modules.
- Keeps the SVG content in separate, readable, deterministic assets.

## Remaining hard limitations
The GitHub README is not an interactive shell: it cannot share state between SVG
images and Markdown. Disclosure arrows remain browser/GitHub chrome and cannot
be restyled by user-defined CSS. Images representing output may still open
their original SVG file when clicked. The inline SVG markup itself has no
clickable controls.

## How to generate and validate
```bash
python3 scripts/make_terminal.py
python3 scripts/validate.py
```

## Manual check after each revision
1. Use GitHub's Preview tab for the README on this branch.
2. Click the command **text** — not the output image.
3. Check that hardware/embedded/software/fabrication and CinemaPi5/LoRa expand.
4. Confirm absence of extra `[run]` labels and grey code pills.
5. Check mobile width and GitHub light/dark themes.
6. If the browser image cache is stale, hard-refresh the README.
