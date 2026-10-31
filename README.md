# Animated terminal for GitHub profiles

A Python-generated SVG based on Debian 13 and XFCE Terminal. The illustration
shows an animated command sequence, a system summary and a Unix directory
listing.

<div align="center">

<img src="./assets/terminal.svg" width="100%" alt="Animated Debian XFCE terminal with commands and project information" />

<a href="https://yassinebkr.github.io/ShellFolio/?run=launch">
  <img src="./assets/pages-cta.svg" width="100%" alt="Open the interactive ShellFolio portfolio" />
</a>

<a href="./docs/README.md">
  <img src="./assets/how-made-it.svg" width="100%" alt="View the SVG generator and documentation" />
</a>

</div>

The SVG is an illustration. For an interactive terminal, follow the
**ShellFolio** link above.

## Customize

| Change | File |
| --- | --- |
| Profile fields and directory names | `scripts/make_terminal.py` |
| Command timing | `scripts/timing.py` |
| Terminal geometry, colors and fonts | `assets/terminal-template.svg` |
| Link to your own portfolio | `README.md` |

## Generate and verify

```bash
python3 scripts/make_terminal.py
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

The generator uses Python's standard library. GitHub Actions checks that
`assets/terminal.svg` matches the source files.

[Profile setup guide](docs/PROFILE-SETUP.md) ·
[Generator details](docs/README.md) ·
[Animation and layout](docs/EXPERIMENT.md) ·
[Artwork credits](docs/DEBIAN-LOGO.md)

## Use in a GitHub profile

Create a public repository with the **same name as your GitHub username**.
Copy the SVG and linked assets into it, then embed them in its `README.md`.
You can keep this generator repository separate from the profile repository.

ShellFolio, the [customizable interactive portfolio](https://github.com/yassinebkr/ShellFolio),
is maintained as a separate project.
