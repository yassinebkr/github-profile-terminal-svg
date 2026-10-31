# Engineering OS — single SVG prototype

## Design goal

The README presents a coherent Debian XFCE terminal scene. Its system summary,
animated command and long-format directory listing share one SVG viewBox,
a fixed monospace grid and a consistent palette.

## Building the asset

```bash
python3 scripts/make_terminal.py
python3 scripts/validate.py
```

The generator uses only the Python standard library. Comments and docstrings
explain the rendering coordinates, animation methods and editable content.

## GitHub rendering

GitHub presents the SVG as an embedded image, including SMIL and CSS animation.
The embedded image displays a complete terminal illustration. Additional
technical content can be introduced through explicitly designed profile
sections as the project develops.

## Engineering constraints

GitHub Markdown supports navigation links and native disclosure elements.
Each mechanism follows GitHub's own UI presentation. The terminal SVG is a
self-contained illustration; its animated appearance serves as the profile's
main experience.

The directory listing's file metadata is illustrative and represents a
fictional Linux workspace. Project claims reflect the documented engineering
experiments, including the validated 45 km LoRa field test.

## Manual review

1. Open the branch's GitHub README preview.
2. Confirm the XFCE chrome and Debian swirl remain visually cohesive.
3. Check the command `ls -l ~/workspace` and its five aligned entries.
4. Verify the cursor animation and introductory command reveal.
5. Inspect both narrow and desktop browser widths.
