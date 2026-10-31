# Animation and layout

The illustration follows a Debian 13 / XFCE Terminal layout. Command output
is shown in a conventional shell transcript.

## Playback sequence

| Step | What appears |
| --- | --- |
| 1 | Shell prompt and typed `neofetch` |
| 2 | Debian logo, system information and color palette |
| 3 | New empty prompt, then typed `ls -l ~/workspace` |
| 4 | Directory listing with Unix permission columns |
| 5 | Final prompt and blinking cursor |

## Timing contract

- A prompt appears shortly after the preceding output.
- The next command starts typing after a brief additional pause.
- Execution pacing depends on the command, **not the output line count**.
- Text appears from left to right and remains visible after completion.
- Reduced-motion settings reveal the completed content.
- Only the cursor blinks indefinitely.

Change `scripts/timing.py` to adjust delays. The SVG stays readable as a
static frame after the animation.

## Visual geometry

| Component | Size |
| --- | --- |
| Terminal SVG | 920 × 626 px |
| Each linked CTA | 920 × 74 px |
| Terminal content | Monospaced text and original Debian vector |

The linked graphics share dimensions for consistent alignment.

## Attribution

The initial concept was inspired by
[AienTech/aientech](https://github.com/AienTech/aientech).
The generator and timeline are independently implemented.

See [Debian vector provenance](DEBIAN-LOGO.md).
