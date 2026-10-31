#!/usr/bin/env python3
"""Generate the Engineering OS terminal graphics for a GitHub profile README.

This self-contained generator was written for the yassinebkr/test experiment.
AienTech's SVG terminal concept inspired this independent implementation.

Generator responsibilities
--------------------------
* Draw a Debian XFCE terminal entirely from editable vector elements.
* Present the engineering profile through a neofetch-style summary.
* Animate command entry using SVG SMIL and cursor blinking using SVG CSS.
* Render realistic long-format Unix directory entries on a monospace grid.
* Produce one deterministic, self-contained SVG with the Python standard library.

GitHub presentation
-------------------
The README displays one image containing the complete terminal interface.
The image presents the portfolio as a visual Linux session.
Each project can subsequently receive a dedicated technical demonstration.

Usage (from the repository root):
    python3 scripts/make_terminal.py
    python3 scripts/validate.py

Requires Python 3.10+ and only the standard library.
"""

from __future__ import annotations

from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET

# Resolve paths from this script for consistent execution from any directory.
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

# --- Editable content -------------------------------------------------------
# Customize the terminal by editing these fields. Running the generator
# then refreshes the SVG assets using the current configuration.

USERNAME = "yassine"
HOSTNAME = "debian"
WINDOW_TITLE = "xfce4-terminal"
PROMPT = f"{USERNAME}@{HOSTNAME}"

SYSTEM_LINES = [
    ("yassine@debian", "green"),
    ("----------------------------", "muted"),
    ("OS:        Debian GNU/Linux 13 (trixie)", "fg"),
    ("Shell:     bash", "fg"),
    ("Focus:     Electronics / Embedded", "fg"),
    ("Hardware:  KiCad / RP2040 / RPi 5", "fg"),
    ("Software:  Python / C / C++ / Linux", "fg"),
    ("Workshop:  CNC / PCB / FDM", "fg"),
    ("Projects:  CinemaPi5 / LoRa 45km", "fg"),
]

# Palette shared by the terminal title bar, shell prompts and listing.
COLORS = {
    "bg": "#0e1116",
    "bar": "#242830",
    "menu": "#181c22",
    "line": "#353d47",
    "fg": "#d5dde6",
    "muted": "#8592a1",
    "green": "#9be5a7",
    "blue": "#91c2ff",
    "pink": "#d67ba1",
    "cyan": "#6fd4dc",
    "yellow": "#f1c77e",
}
COLORS["dir"] = COLORS["blue"]
COLORS["ok"] = COLORS["green"]
COLORS["header"] = COLORS["cyan"]
COLORS["hint"] = COLORS["muted"]
COLORS["warn"] = COLORS["yellow"]

WIDTH = 900

# Keys shared by directory image assets and README section anchors.
DIRECTORIES = ('hardware', 'embedded', 'software', 'fabrication', 'projects')

# --- SVG building blocks ----------------------------------------------------
# XML escaping matters here. A user's project description may contain "&" or
# "<", which would otherwise produce malformed SVG or unexpected markup.


def rectangle(x: float, y: float, width: float, height: float,
              color: str, extra: str = "") -> str:
    """Return a filled rectangle; extra contains trusted SVG attributes."""
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
        f'fill="{color}" {extra}/>'
    )


def text_at(x: float, y: float, value: str, color: str | None = None,
            size: int = 15, weight: int = 400) -> str:
    """Draw one monospace line, with all visible content XML-escaped."""
    chosen = color or COLORS["fg"]
    return (
        f'<text x="{x}" y="{y}" fill="{chosen}" '
        f'font-size="{size}" font-weight="{weight}">'
        f'{escape(value, quote=True)}</text>'
    )


def document(height: int, contents: str) -> str:
    """Wrap terminal drawing elements in a standalone, valid SVG document.

    The CSS animation applies only to the blinking cursor. SVG/SMIL typing
    is defined inside the hero's clipPath below. Reduced-motion users see
    a steady cursor instead of the blinking animation.
    """
    css = (
        "text{font-family:'DejaVu Sans Mono','Liberation Mono',"
        "Consolas,monospace}"
        "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}"
        ".cursor{animation:blink 1.1s steps(1) infinite}"
        "@media(prefers-reduced-motion:reduce){.cursor{animation:none}}"
    )
    # The single SVG includes a complete terminal window and its content.
    background = rectangle(
        0.5, 0.5, WIDTH - 1, height - 1, COLORS["bg"],
        f'rx="8" stroke="{COLORS["line"]}"',
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{WIDTH}" height="{height}" '
        f'viewBox="0 0 {WIDTH} {height}" role="img">'
        f'<title>Debian terminal / Engineering OS</title>'
        f"<style>{css}</style>{background}{contents}</svg>\n"
    )


# --- Terminal window and animated home screen -------------------------------

def render_home() -> str:
    """Build one continuous Debian XFCE terminal scene.

    The terminal is a single self-contained SVG asset. Every line shares the
    same font grid, palette, image coordinate system and outer window frame.
    A realistic Unix long listing follows the neofetch-style profile summary.
    """
    svg = rectangle(1, 1, 898, 34, COLORS["bar"], 'rx="8"')
    svg += rectangle(1, 29, 898, 7, COLORS["bar"])
    svg += rectangle(1, 35, 898, 26, COLORS["menu"])

    # Use the standard XFCE-style right-hand window management controls.
    svg += text_at(16, 23, "▣", COLORS["green"], weight=700)
    svg += text_at(40, 23, f"{PROMPT}: ~ — {WINDOW_TITLE}", size=13)
    for x, symbol in [(813, "─"), (846, "□"), (875, "×")]:
        svg += text_at(x, 23, symbol, COLORS["muted"])
    svg += text_at(18, 53, "File   Edit   View   Terminal   Tabs   Help",
                   COLORS["muted"], size=12)

    svg += text_at(25, 95, PROMPT, COLORS["green"])
    svg += text_at(160, 95, ":~$", COLORS["blue"])

    # SMIL animates a clipping mask to reveal the pre-rendered command.
    # The same image animates directly in supporting Markdown viewers.
    svg += (
        '<defs><clipPath id="typing">'
        '<rect x="207" y="74" width="203" height="26">'
        '<animate attributeName="width" values="0;0;35;70;110;150;203" '
        'keyTimes="0;0.18;0.36;0.52;0.68;0.84;1" '
        'dur="2.3s" fill="freeze"/>'
        '</rect></clipPath></defs>'
        '<g clip-path="url(#typing)">'
    )
    svg += text_at(207, 95, "neofetch --engineer")
    svg += "</g>"

    # The Debian-inspired spiral is drawn from resolution-independent paths.
    svg += (
        f'<g transform="translate(58 138)" stroke="{COLORS["pink"]}" '
        'stroke-width="9" stroke-linecap="round" fill="none">'
        '<path d="M125 7C62 -12 8 32 7 91c-1 65 80 99 130 50 '
        '37-37 33-89-6-104-32-12-70 10-65 40 '
        '4 28 41 35 59 17"/>'
        '<path d="M127 9c17 9 30 20 36 38" '
        'opacity=".7" stroke-width="5"/></g>'
    )
    svg += text_at(63, 324, "DEBIAN 13", COLORS["pink"], size=20, weight=700)

    # Position system properties on the same fixed-height terminal grid.
    for index, (line, palette) in enumerate(SYSTEM_LINES):
        svg += text_at(293, 142 + 24 * index, line,
                       COLORS[palette], size=14,
                       weight=700 if index == 0 else 400)

    palette = ["pink", "yellow", "green", "cyan", "blue"]
    for index, color in enumerate(palette):
        svg += rectangle(293 + 34 * index, 363, 33, 13, COLORS[color])
    for index, color in enumerate(["#b4a7ee", "#d7dce4", "#7e8997"], 5):
        svg += rectangle(293 + 34 * index, 363, 33, 13, color)

    # The long-format listing uses the usual Unix columns:
    # permission bits, hard-link count, owner, group, size, date, filename.
    # These representative values describe a simulated engineering workspace.
    svg += text_at(25, 408, PROMPT, COLORS["green"])
    svg += text_at(160, 408, ":~$", COLORS["blue"])
    svg += text_at(207, 408, "ls -l ~/workspace")
    svg += text_at(25, 440, "total 20", COLORS["muted"], size=14)

    prefix = "drwxr-xr-x  2 yassine yassine 4096 Oct 31 "
    filename_x = 25 + len(prefix) * 8.4
    for index, directory in enumerate(DIRECTORIES):
        baseline = 470 + index * 25
        svg += text_at(25, baseline, prefix, COLORS["muted"], size=14)
        svg += text_at(filename_x, baseline, directory + "/",
                       COLORS["blue"], size=14)

    # Finish the session inside the same canvas and keep the cursor animated.
    svg += text_at(25, 632, "visitor@debian", COLORS["green"])
    svg += text_at(160, 632, ":~$", COLORS["blue"])
    svg += rectangle(207, 617, 9, 17, COLORS["green"], 'class="cursor"')
    return document(653, svg)


def main() -> None:
    """Build, XML-validate and save all files in a deterministic order."""
    ASSETS.mkdir(parents=True, exist_ok=True)

    images: dict[str, str] = {"terminal.svg": render_home()}

    for filename, markup in sorted(images.items()):
        # Validate before overwriting the previous good asset.
        ET.fromstring(markup)
        destination = ASSETS / filename
        destination.write_text(markup, encoding="utf-8")
        print(f"generated: {destination.relative_to(ROOT)}")

    print(f"Done: {len(images)} SVG image generated.")


if __name__ == "__main__":
    main()
