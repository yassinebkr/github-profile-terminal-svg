#!/usr/bin/env python3
"""Generate the Engineering OS terminal graphics for a GitHub profile README.

This is a self-contained generator written for the yassinebkr/test experiment.
It is NOT a copy or a Python port of AienTech's make_terminal.py.

What this program does
----------------------
* Draw an XFCE-inspired Linux terminal entirely with SVG elements.
* Reproduce a Debian-themed "neofetch" view using editable profile data.
* Use SMIL to reveal a typed command and CSS to blink the shell cursor.
* Produce SVG representations of system directories and project case studies.
* Keep every generated image deterministic and free of external dependencies.

What it deliberately does NOT do
--------------------------------
* Execute Linux commands or JavaScript inside GitHub.
* Make SVG elements clickable when embedded with <img>.
* Modify README.md or simulate a working shell input widget.

Real README interactivity is provided by HTML <details>/<summary>, with plain
text inside <summary>. GitHub can wrap SVG images in links to the SVG file,
so putting images *inside* <summary> is not a reliable clickable control.

Usage (from the repository root):
    python3 scripts/make_terminal.py
    python3 scripts/validate.py

Requires Python 3.10+ and only the standard library.
"""

from __future__ import annotations

from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET

# All paths are relative to this script, not the caller's working directory.
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

# --- Editable content -------------------------------------------------------
# Edit these fields to personalize the header. Do not edit the SVG files
# directly: a subsequent generator run would overwrite manual modifications.

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

# Each panel is (command, lines). Each line may be plain text or a pair
# (semantic_kind, line_text). The semantic kind chooses a terminal color.
PANELS = {
    "skills": (
        "ls -la ~/workspace/",
        [
            "total 5   drwxr-xr-x   engineering environments",
            ("dir", " hardware/      KiCad / SPICE / electronics"),
            ("dir", " embedded/      RP2040 / sensors / radio"),
            ("dir", " software/      Python / C / C++ / Linux"),
            ("dir", " fabrication/   CNC / Fusion 360 / FDM"),
            ("dir", " projects/      validated case studies"),
            ("hint", "Select a command below to inspect a subsystem."),
        ],
    ),
    "hardware": (
        "cat ~/workspace/hardware/README",
        [
            ("header", "/hardware — circuit design and integration"),
            ("ok", "[OK] KiCad schematic and PCB design"),
            ("ok", "[OK] Circuit simulation / SPICE"),
            ("ok", "[OK] I2C, SPI, UART, RS-485"),
            ("ok", "[OK] Reflow, soldering and PCB bring-up"),
            ("hint", "Workflow: design > assemble > validate"),
        ],
    ),
    "embedded": (
        "cat ~/workspace/embedded/README",
        [
            ("header", "/embedded — embedded hardware and software"),
            ("ok", "[OK] Raspberry Pi 5 / RP2040"),
            ("ok", "[OK] Embedded Linux / camera sensor drivers"),
            ("ok", "[OK] IMU / GNSS / LoRa telemetry"),
            ("ok", "[OK] TCP / Ethernet / UART"),
            ("hint", "Evidence: IMX283 camera + 45 km LoRa field test"),
        ],
    ),
    "projects": (
        "ls ~/projects/",
        [
            "PROJECT INDEX",
            ("dir", "01  cinemapi5/   DIY cinema camera engineering"),
            ("dir", "02  lora/        Long-range radio telemetry"),
            ("hint", "Select a project below for implementation details."),
        ],
    ),
    "camera": (
        "inspect ~/projects/cinemapi5",
        [
            ("header", "CINEMAPI5 / R&D PROTOTYPE"),
            ("ok", "Platform       Raspberry Pi 5 + NVMe"),
            ("ok", "Sensor         Sony IMX283"),
            ("ok", "Imaging        RAW / Libcamera / PISP"),
            ("ok", "UI             Responsive web / PWA"),
            ("ok", "Integration    LUT / IMU / HUD"),
            ("warn", "Target         4K 12-bit 30fps (performance goal)"),
            ("hint", "Code: github.com/yassinebkr/cinematepi5"),
        ],
    ),
    "lora": (
        "inspect ~/projects/lora",
        [
            ("header", "LONG-RANGE TELEMETRY / FIELD-VALIDATED"),
            ("ok", "Platform       RP2040 (TX and RX)"),
            ("ok", "Radio          RFM95 / 868 MHz"),
            ("ok", "Sensors        IMU + GNSS"),
            ("ok", "Antenna        Directional Yagi"),
            ("cyan", "TX [RP2040] )))) 868 MHz (((( [RP2040] RX"),
            ("ok", "[PASS] 45 km wireless link validated"),
            ("hint", "A measured field result, not a theoretical range"),
        ],
    ),
}

# These hexadecimal colors match the SVG version already committed to GitHub.
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
    """Produce the 900 x 496 px XFCE terminal with the Debian-style graphic."""
    svg = rectangle(1, 1, 898, 34, COLORS["bar"], 'rx="8"')
    svg += rectangle(1, 29, 898, 7, COLORS["bar"])
    svg += rectangle(1, 35, 898, 26, COLORS["menu"])

    # XFCE-style controls go on the RIGHT. There are no macOS traffic lights.
    svg += text_at(16, 23, "▣", COLORS["green"], weight=700)
    svg += text_at(40, 23, f"{PROMPT}: ~ — {WINDOW_TITLE}", size=13)
    for x, symbol in [(813, "─"), (846, "□"), (875, "×")]:
        svg += text_at(x, 23, symbol, COLORS["muted"])
    svg += text_at(18, 53, "File   Edit   View   Terminal   Tabs   Help",
                   COLORS["muted"], size=12)

    svg += text_at(25, 95, PROMPT, COLORS["green"])
    svg += text_at(160, 95, ":~$", COLORS["blue"])

    # The command already exists in the SVG. SMIL progressively widens a
    # clipping rectangle so the text looks as though someone is typing it.
    # This is visual animation, not JavaScript and not actual keyboard input.
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

    # Original minimalist Debian-inspired mark, drawn with vector paths.
    # It is not a screenshot or a raster image.
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

    # Neofetch-style system properties. Every row starts at a fixed x/y.
    for index, (line, palette) in enumerate(SYSTEM_LINES):
        svg += text_at(293, 142 + 24 * index, line,
                       COLORS[palette], size=14,
                       weight=700 if index == 0 else 400)

    # The familiar terminal palette is built from eight SVG rectangles.
    swatches = ["pink", "yellow", "green", "cyan", "blue"]
    for index, color in enumerate(swatches):
        svg += rectangle(293 + 34 * index, 363, 33, 13, COLORS[color])
    for index, color in enumerate(["#b4a7ee", "#d7dce4", "#7e8997"], 5):
        svg += rectangle(293 + 34 * index, 363, 33, 13, color)

    svg += text_at(25, 408, PROMPT, COLORS["green"])
    svg += text_at(160, 408, ":~$", COLORS["blue"])
    svg += text_at(207, 408, "ls ~/workspace")
    svg += text_at(
        25, 437, "hardware/ embedded/ software/ fabrication/ projects/",
        COLORS["blue"], size=14,
    )
    svg += text_at(25, 470, "visitor@debian", COLORS["green"])
    svg += text_at(160, 470, ":~$", COLORS["blue"])
    svg += text_at(207, 470, "select a command below", COLORS["muted"], size=14)

    # CSS controls the blink. The cursor has no input behavior.
    svg += rectangle(410, 455, 9, 17, COLORS["green"], 'class="cursor"')
    return document(496, svg)


# --- Command and output graphics -------------------------------------------
# The command images are retained for experiments and comparison, even though
# README.md now uses plain <summary><code>...</code></summary> so that clicking
# the text actually expands the section instead of opening an SVG file.


def render_command(command: str) -> str:
    """Render a shell prompt strip (not used as an interactive HTML button)."""
    svg = text_at(22, 34, "visitor@debian", COLORS["green"], weight=700)
    svg += text_at(158, 34, ":~$", COLORS["blue"])
    svg += text_at(209, 34, command)
    svg += text_at(785, 34, "[ ENTER ]", COLORS["green"], size=12, weight=700)
    return document(56, svg)


def render_output(name: str, lines: list[str | tuple[str, str]]) -> str:
    """Render a fixed-width shell stdout panel for a documented project."""
    height = 100 + len(lines) * 25
    svg = rectangle(14, 16, 3, height - 52, COLORS["green"])
    svg += text_at(30, 29, f"stdout  /  {name}", COLORS["muted"], size=12)

    for index, entry in enumerate(lines):
        # A bare string denotes a header; tuples name a semantic color.
        kind, line = entry if isinstance(entry, tuple) else ("header", entry)
        svg += text_at(30, 65 + index * 25, line,
                       COLORS.get(kind, COLORS["fg"]), size=14)

    svg += text_at(30, height - 17, "process exited with code 0",
                   COLORS["muted"], size=11)
    return document(height, svg)


def main() -> None:
    """Build, XML-validate and save all files in a deterministic order."""
    ASSETS.mkdir(parents=True, exist_ok=True)

    images: dict[str, str] = {"terminal.svg": render_home()}
    for name, (command, lines) in PANELS.items():
        images[f"cmd-{name}.svg"] = render_command(command)
        images[f"out-{name}.svg"] = render_output(name, lines)

    for filename, markup in sorted(images.items()):
        # Validate before overwriting the previous good asset.
        ET.fromstring(markup)
        destination = ASSETS / filename
        destination.write_text(markup, encoding="utf-8")
        print(f"generated: {destination.relative_to(ROOT)}")

    print(f"Done: {len(images)} SVG images generated.")


if __name__ == "__main__":
    main()
