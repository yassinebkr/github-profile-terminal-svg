# Interactive Debian README — experiment

Branch: `experiment/interactive-terminal`. `main` is intentionally unchanged.

## Interaction model
A full-width animated SVG is the terminal home screen. Every click target is an SVG inside a native Markdown `<summary>`. Expanding a `<details>` reveals an SVG shell output and optionally nested commands.

## Manual test on GitHub
1. Open this branch's rendered README (**Preview**, not Code).
2. Confirm XFCE controls are on the right: minimize / maximize / close; no macOS traffic lights.
3. Reload and check the typewriter/cursor animation (unless reduced-motion settings are enabled).
4. Click the command image `ls -la ~/workspace/`. Check whether the output becomes visible.
5. Click nested `hardware` and `embedded` command images. Check they expand and collapse.
6. Expand projects and select CinemaPi5 / LoRa.
7. Test GitHub light and dark themes and a narrow mobile viewport.

## Technical limits
- SVG embedded with an image tag cannot accept meaningful internal pointer actions.
- Commands are *pre-defined disclosure controls*, not actual shell input.
- GitHub's image proxy, cache, HTML sanitizer and browser SVG support may affect appearance and animation.
- Clickability and layout of images nested in `<summary>` must be confirmed in the real GitHub renderer.
- No scripts or network calls execute in this README.

## Next steps
Reduce apparent disclosure markers, align output shells, add a generator for consistent graphics, expand software/fabrication modules, improve keyboard navigation, test animation fallback.
