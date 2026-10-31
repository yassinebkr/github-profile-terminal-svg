# Generator reference

## Project map

| File | Purpose |
| --- | --- |
| `scripts/make_terminal.py` | Profile content and SVG assembly |
| `scripts/timing.py` | Prompt, typing and response timing |
| `scripts/make_cta.py` | Standalone CTA arrow geometry and customization |
| `scripts/validate.py` | SVG integrity and security checks |
| `tests/test_timing.py` | Timing and typing regression tests |
| `tests/test_cta.py` | CTA arrow customization and bounds tests |
| `assets/terminal-template.svg` | XFCE-style layout and animation groups |
| `assets/debian-open-use.svg` | Debian vector artwork |
| `assets/terminal.svg` | Generated profile illustration |
| `assets/shellfolio-cta-arrows-v3.svg` | Generated CTA linking to the interactive portfolio |
| `assets/source-button.svg` | Compact link to the generator repository from a profile README |

## Regenerate

```bash
python3 scripts/make_terminal.py
python3 scripts/make_cta.py
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

Use Python 3. No additional packages are required.

## Personalize

Edit the constants at the top of `scripts/make_terminal.py`:

- `USER`, `HOST`, `WINDOW_TITLE`
- `SYSTEM_FIELDS`: system and project information
- `DIRECTORIES`: long-format listing content

Use `scripts/timing.py` to adjust the pauses. The renderer positions
text independently from event times. Do not edit generated SVGs manually.

CTA arrows live in a separate, lightweight generator: edit `MAIN_ARROW` and
`INLINE_ARROW` in `scripts/make_cta.py`. Each has `direction` (`up`,
`down`, `left`, `right`), `length` (even number of pixels, 8–36),
`stroke`, `color`, and fixed-position `x`/`y` coordinates. Invalid
values and arrows extending outside the button are rejected. A single
vector shape is rotated instead of maintaining four path variants.

## Profile integration

The illustration is a standalone image. Markdown links under it can open a
separate website such as [ShellFolio](https://yassinebkr.github.io/ShellFolio/).

For GitHub to show a profile README, its repository name must match your
account username. The generator itself can have any repository name.

See [profile setup](PROFILE-SETUP.md), [animation choices](EXPERIMENT.md) and
[Debian logo attribution](DEBIAN-LOGO.md).
