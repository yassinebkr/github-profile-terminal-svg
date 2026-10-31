# XFCE profile terminal — SVG design notes

## Presentation

The README displays one standalone SVG with a Debian-inspired XFCE terminal
window, vector Debian swirl and an illustrated long-format Unix listing.
The window chrome, menu strip, text alignment and palette use the user's
XFCE Terminal screenshot as their visual reference.

## Generator

```bash
python3 scripts/make_terminal.py
python3 scripts/validate.py
```

- `assets/terminal-template.svg`: geometry, CSS, animation and window chrome
- `assets/debian-open-use.svg`: source vector for the Debian swirl
- `assets/terminal.svg`: deterministic generated SVG
- `scripts/make_terminal.py`: editable profile fields and XML composition
- `scripts/validate.py`: structural and reproducibility checks

The username `yassine@debian`, animated `neofetch` command, vector terminal
glyph and shell cursor are kept consistent across the generated scene.
The typing clip covers the complete eight-character command.

## GitHub profile navigation

The README uses two independent SVG-linked rows:

1. **Open ShellFolio** — the separate public interactive portfolio at
   https://yassinebkr.github.io/ShellFolio/
2. **How I made it** — the Python source and documentation for this generated
   profile asset, in the current repository.

GitHub Markdown offers a constrained interaction surface. The richer
browser terminal, its JavaScript interpreter, the replay animation and its
tests are maintained exclusively in https://github.com/yassinebkr/ShellFolio.

## Acknowledgements

The first prototype was inspired by
[AienTech/aientech](https://github.com/AienTech/aientech).
This generator and its window geometry were independently implemented.
Refer to [DEBIAN-LOGO.md](DEBIAN-LOGO.md) for logo provenance.
