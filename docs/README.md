# ShellFolio — development workspace

This private repository contains the animated GitHub-profile SVG, its
Python generator, the source of the ShellFolio interactive browser terminal,
and the associated tests and technical documentation.

## Structure

- `assets/` — generated SVG hero, template, logo artwork and README launcher
- `scripts/` — Python SVG generator and validation utilities
- `web/` — HTML, CSS, JavaScript modules and Debian vector for the browser application
- `tests/` — virtual filesystem and command interpreter tests
- `docs/` — developer documentation, design experiments and credits
- `.github/workflows/` — CI verification

Python generates the self-contained animated profile SVG. JavaScript runs the
virtual terminal inside a web browser, supporting shell commands, virtual
navigation, history and tab completion.

## Development

```bash
python3 scripts/make_terminal.py
python3 scripts/validate.py
npm test
python3 -m http.server 8000 --directory web
```

The interactive application then opens at http://localhost:8000/.

## Public site

Live URL (after GitHub Pages activation):
https://yassinebkr.github.io/ShellFolio/

Public site-only repository: https://github.com/yassinebkr/ShellFolio

Keep this repository private during the ongoing development and documentation
phase. The public repository contains the static application only. Review
documentation and licenses before any future release of the full development
repository.

## Acknowledgements

Special thanks to [AienTech](https://github.com/AienTech), whose animated
terminal in [AienTech/aientech](https://github.com/AienTech/aientech)
inspired the original GitHub profile experiment. The Python SVG rendering
pipeline and browser-based virtual terminal are independent implementations.

See [DEBIAN-LOGO.md](DEBIAN-LOGO.md) for Debian artwork provenance.
