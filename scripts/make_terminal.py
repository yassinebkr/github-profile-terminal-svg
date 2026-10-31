#!/usr/bin/env python3
"""Build the animated Debian/XFCE GitHub profile terminal.

The geometry and colors are modeled after an XFCE Terminal reference
screenshot. The Debian swirl uses an authentic vector path preserved in
assets/debian-open-use.svg.

The generator injects the profile, Unix directory records and Debian
geometry into a standalone SVG template. The generated terminal image
uses SVG SMIL and CSS for animation and the Python standard library
for asset construction.

Run from the repository root:
    python3 scripts/make_terminal.py
    python3 scripts/validate.py
"""

from __future__ import annotations

from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
TEMPLATE_PATH = ASSETS / "terminal-template.svg"
ICON_PATH = ASSETS / "debian-open-use.svg"
OUTPUT_PATH = ASSETS / "terminal.svg"

# Editable profile fields allow quick customization of the terminal.
# INPUT_X derives from the complete prompt at 15px DejaVu Sans Mono spacing,
# keeping animated commands and the final cursor aligned with the shell.
USER = "yassine"
HOST = "debian"
WINDOW_TITLE = "Terminal - yassine@debian: ~"

SYSTEM_FIELDS: tuple[tuple[str, str], ...] = (
    ("OS", "Debian GNU/Linux 13 (trixie)"),
    ("Shell", "bash"),
    ("DE", "Xfce"),
    ("Terminal", "xfce4-terminal"),
    ("Focus", "Electronics / Embedded Systems"),
    ("Toolchain", "KiCad / Python / C / C++"),
    ("Projects", "CinemaPi5 / LoRa telemetry"),
)

# Permissions, owners and dates model an illustrative GNU/Linux workspace.
# Each entry follows the familiar column layout of the GNU coreutils ls tool.
DIRECTORIES: tuple[tuple[str, str], ...] = (
    ("Sep 21", "hardware/"),
    ("Oct 19", "embedded/"),
    ("Oct 22", "software/"),
    ("Oct 24", "fabrication/"),
    ("Oct 29", "projects/"),
)


def load_debian_path() -> str:
    """Extract the original vector path from the locally stored logo SVG."""
    root = ET.parse(ICON_PATH).getroot()
    ns = "{http://www.w3.org/2000/svg}"
    paths = root.findall(f".//{ns}path")
    if len(paths) != 1 or "d" not in paths[0].attrib:
        raise ValueError("Expected one Debian vector path in the source SVG")
    return paths[0].attrib["d"]


def render_system_rows() -> str:
    """Render aligned system-property labels using a monospace column grid."""
    rows: list[str] = []
    for index, (label, value) in enumerate(SYSTEM_FIELDS):
        y = 205 + index * 23
        dx = f"{max(1, 10 - len(label)) * 8.45:.2f}"
        rows.append(
            f'<text x="335" y="{y}" class="body" xml:space="preserve">'
            f'<tspan class="key">{escape(label)}:</tspan>'
            f'<tspan dx="{dx}">{escape(value)}</tspan></text>'
        )
    return "\n  ".join(rows)


def render_listing_rows() -> str:
    """Produce realistic listing columns and distinct directory coloring.

    Every row shares one SVG text element and baseline. This preserves the
    natural continuity of a real shell's monospaced directory listing.
    """
    rows: list[str] = []
    for index, (date, directory) in enumerate(DIRECTORIES):
        baseline = 476 + index * 24
        owner = USER.ljust(8)
        columns = f"drwxr-xr-x  2 {owner} {owner} 4096 {date}  "
        rows.append(
            f'<text x="25" y="{baseline}" class="listing" xml:space="preserve">'
            f'<tspan class="permissions">{escape(columns)}</tspan>'
            f'<tspan class="directory">{escape(directory)}</tspan></text>'
        )
    return "\n  ".join(rows)


def build_terminal() -> str:
    """Combine the template, profile fields and Debian vector geometry."""
    result = TEMPLATE_PATH.read_text(encoding="utf-8")
    replacements = {
        "{{WINDOW_TITLE}}": escape(WINDOW_TITLE, quote=True),
        "{{INPUT_X}}": f"{25 + len(f'{USER}@{HOST}:~$ ') * 9.03:.2f}",
        "{{SHELL_USER_HOST}}": escape(f"{USER}@{HOST}", quote=True),
        "{{DEBIAN_PATH}}": escape(load_debian_path(), quote=True),
        "{{SYSTEM_ROWS}}": render_system_rows(),
        "{{LISTING_ROWS}}": render_listing_rows(),
    }
    for marker, value in replacements.items():
        result = result.replace(marker, value)

    if "{{" in result:
        raise ValueError("An SVG template token remains unresolved")
    ET.fromstring(result)
    return result


def main() -> None:
    """Regenerate and XML-validate the self-contained terminal SVG asset."""
    output = build_terminal()
    OUTPUT_PATH.write_text(output, encoding="utf-8")
    print(f"generated {OUTPUT_PATH.relative_to(ROOT)} ({len(output)} bytes)")


if __name__ == "__main__":
    main()
