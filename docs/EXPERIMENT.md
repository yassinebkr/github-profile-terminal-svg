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
| Each linked CTA | 296 × 62 px |
| Terminal content | Monospaced text and original Debian vector |

Both linked graphics use the same intrinsic size. In a profile README,
render them at that explicit size, next to each other inside a centered
paragraph. On narrow screens they can wrap independently.

## Attribution

The initial concept was inspired by the talented
[AienTech](https://github.com/AienTech), especially their original
[AienTech/aientech profile](https://github.com/AienTech/aientech).
The generator and timeline here are independently implemented.

See [Debian vector provenance](DEBIAN-LOGO.md).
