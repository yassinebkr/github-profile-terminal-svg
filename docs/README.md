# Generator reference

## Project map

| File | Purpose |
| --- | --- |
| `scripts/make_terminal.py` | Profile content and SVG assembly |
| `scripts/timing.py` | Prompt, typing and response timing |
| `scripts/validate.py` | SVG integrity and security checks |
| `tests/test_timing.py` | Timing and typing regression tests |
| `assets/terminal-template.svg` | XFCE-style layout and animation groups |
| `assets/debian-open-use.svg` | Debian vector artwork |
| `assets/terminal.svg` | Generated profile illustration |
| `assets/pages-cta.svg` | Link to ShellFolio |
| `assets/how-made-it.svg` | Link to this documentation |

## Regenerate

```bash
python3 scripts/make_terminal.py
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
text independently from event times. Do not edit the generated SVG manually.

## Profile integration

The illustration is a standalone image. Markdown links under it can open a
separate website such as [ShellFolio](https://yassinebkr.github.io/ShellFolio/).

For GitHub to show a profile README, its repository name must match your
account username. The generator itself can have any repository name.

See [profile setup](PROFILE-SETUP.md), [animation choices](EXPERIMENT.md) and
[Debian logo attribution](DEBIAN-LOGO.md).
