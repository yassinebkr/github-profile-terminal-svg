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
assert "Terminal - yassine@debian: ~" in svg, "Incorrect XFCE title"
assert svg.count("yassine@debian") >= 4, "Profile prompt mismatch"
# The final clipping width covers all eight glyphs of the neofetch command.
svg_ns = "{http://www.w3.org/2000/svg}"
type_clip = root.find(f".//{svg_ns}clipPath[@id='typeNeofetch']/{svg_ns}rect/{svg_ns}animate")
assert type_clip is not None, "SMIL typing animation missing"
assert float(type_clip.attrib["values"].split(";")[-1]) >= 76, "Last typed character gets clipped"
# The icon is constructed from vector geometry for consistent GitHub scaling.
icon_group = [group for group in root.findall(f".//{svg_ns}g") if group.attrib.get("aria-label") == "XFCE terminal application icon"]
assert len(icon_group) == 1, "XFCE terminal application icon missing"
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
# Related README link graphics must share exact dimensions and geometry.
for asset in ("pages-cta.svg", "how-made-it.svg"):
    graphic = ET.parse(ROOT / "assets" / asset).getroot()
    assert graphic.attrib.get("viewBox") == "0 0 920 74", f"Misaligned CTA: {asset}"
    assert graphic.attrib.get("height") == "74", f"Inconsistent height: {asset}"
assert "ShellFolio/?run=launch" in readme, "The public site must run its virtual launcher"
print("validated vector logo, GTK chrome, Unix listing, aligned links, and README")
