#!/usr/bin/env python3
"""Generate the compact ShellFolio CTA without changing terminal animation.

Edit only MAIN_ARROW and INLINE_ARROW for the arrow direction, size or color.
Standard-library only; output is a standalone, deterministic SVG.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "assets" / "shellfolio-cta-arrows-v3.svg"
ROTATION = {"right": 0, "down": 90, "left": 180, "up": -90}


@dataclass(frozen=True)
class Arrow:
    identifier: str
    x: int
    y: int
    direction: str
    length: int
    stroke: float
    color: str


# The large green arrow uses the same 20px/2.3px proportions as the
# pink arrow on source-button.svg, rotated upward.
MAIN_ARROW = Arrow("terminal-up-arrow", 269, 31, "up", 20, 2.3, "#72df91")
# Short, white inline right arrow after "OR CLICK HERE TO OPEN".
INLINE_ARROW = Arrow("button-open-arrow", 165, 42, "right", 14, 1.7, "#e5eaf0")


def render_arrow(spec: Arrow) -> str:
    """Rotate a single right-pointing vector shape around its center."""
    if spec.direction not in ROTATION:
        raise ValueError("direction must be right, down, left or up")
    if type(spec.length) is not int or not 8 <= spec.length <= 36 or spec.length % 2:
        raise ValueError("arrow length must be an even integer from 8 to 36")
    if type(spec.x) is not int or type(spec.y) is not int:
        raise ValueError("arrow coordinates must be integers")
    half = spec.length // 2
    head = int(spec.length * 0.4)
    horizontal = spec.direction in ("left", "right")
    x_span, y_span = (half, head) if horizontal else (head, half)
    if not (8 <= spec.x - x_span and spec.x + x_span <= 288
            and 8 <= spec.y - y_span and spec.y + y_span <= 54):
        raise ValueError("arrow would extend outside the button's safe area")
    if type(spec.stroke) not in (float, int) or not 0.5 <= spec.stroke <= 4:
        raise ValueError("arrow stroke must be between 0.5 and 4")
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", spec.color):
        raise ValueError("arrow color must be a six-digit hex value")
    if not re.fullmatch(r"[a-z][a-z0-9-]*", spec.identifier):
        raise ValueError("arrow identifier must be a safe SVG id")

    path = (
        f"M{spec.x - half} {spec.y}h{spec.length}"
        f"m-{head}-{head} {head} {head}-{head} {head}"
    )
    degrees = ROTATION[spec.direction]
    transform = f' transform="rotate({degrees} {spec.x} {spec.y})"' if degrees else ""
    return (
        f'<path id="{spec.identifier}" d="{path}"{transform} '
        f'stroke="{spec.color}" stroke-width="{spec.stroke:g}" '
        'fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    )


def build_cta(main: Arrow = MAIN_ARROW, inline: Arrow = INLINE_ARROW) -> str:
    """Build the two-arrow card; preserve the standard 296 x 62 geometry."""
    if main.identifier == inline.identifier:
        raise ValueError("arrow ids must be unique")
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="296" height="62" '
        'viewBox="0 0 296 62" role="img" aria-labelledby="title description">\n'
        '<title id="title">Click the terminal above, or click here, to open ShellFolio</title>\n'
        '<desc id="description">This linked button opens ShellFolio. '
        'The upper arrow points to the animated terminal; the lower arrow '
        'identifies this button as clickable.</desc>\n'
        '<rect x="0.75" y="0.75" width="294.5" height="60.5" '
        'rx="6" fill="#0c1117" stroke="#394550" stroke-width="1.5"/>\n'
        '<path d="M8 14v34" stroke="#72df91" stroke-width="3" '
        'stroke-linecap="round"/>\n'
        '<text x="22" y="27" '
        'font-family="DejaVu Sans Mono,Liberation Mono,monospace" '
        'font-size="14" font-weight="600" fill="#e5eaf0">'
        'Click terminal above</text>\n'
        '<text x="22" y="45" '
        'font-family="DejaVu Sans Mono,Liberation Mono,monospace" '
        'font-size="10" fill="#a5b2bf">OR CLICK HERE TO OPEN</text>\n'
        f'{render_arrow(main)}\n'
        f'{render_arrow(inline)}\n'
        '</svg>\n'
    )
    ET.fromstring(svg)
    return svg


def main() -> None:
    OUTPUT_PATH.write_text(build_cta(), encoding="utf-8")
    print(f"generated {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
