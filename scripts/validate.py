#!/usr/bin/env python3
"""Validate the deterministic Debian XFCE terminal build."""

import re
from pathlib import Path
from xml.etree import ElementTree as ET

from make_terminal import ROOT, OUTPUT_PATH, build_terminal

svg = OUTPUT_PATH.read_text(encoding="utf-8")
assert svg == build_terminal(), "Regenerate terminal.svg from its template"
root = ET.fromstring(svg)
assert root.attrib["viewBox"] == "0 0 920 668", "Unexpected image geometry"
assert 'fill="#d70751"' in svg, "Debian vector color is missing"
assert '<path d="' in svg, "Debian path element is missing"
assert 'clipPath id="typeNeofetch"' in svg, "SMIL typing clip is missing"
assert 'class="cursor"' in svg, "Shell cursor is missing"
assert "ls -l ~/workspace" in svg, "Long-format directory listing is missing"
for directory in ("hardware/", "embedded/", "software/", "fabrication/", "projects/"):
    assert directory in svg, f"Missing directory: {directory}"
assert svg.count("<script") == 0, "Script elements detected"
assert svg.count("<foreignObject") == 0, "Foreign objects detected"
assert re.search(r'(?:href|src)=["\']https?://', svg) is None, "External resource detected"

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for relative in re.findall(r'src="([^"]+)"', readme):
    assert (ROOT / relative).exists(), f"Missing README asset: {relative}"
print("validated vector logo, GTK chrome, Unix listing, animations, and README")
