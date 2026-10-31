#!/usr/bin/env python3
"""Validate the deterministic Debian XFCE terminal build."""

import re
from pathlib import Path
from xml.etree import ElementTree as ET

from make_terminal import ROOT, OUTPUT_PATH, build_terminal, USER, HOST, WINDOW_TITLE, DIRECTORIES
from make_cta import build_cta, OUTPUT_PATH as CTA_OUTPUT_PATH

svg = OUTPUT_PATH.read_text(encoding="utf-8")
assert svg == build_terminal(), "Regenerate terminal.svg from its template"
root = ET.fromstring(svg)
assert root.attrib["viewBox"] == "0 0 920 626", "Unexpected image geometry"
assert 'fill="#d70751"' in svg, "Debian vector color is missing"
assert '<path d="' in svg, "Debian path element is missing"
assert 'clipPath id="typeNeofetch"' in svg, "SMIL typing clip is missing"
assert WINDOW_TITLE in svg, "Incorrect XFCE title"
assert svg.count(f"{USER}@{HOST}") >= 4, "Profile prompt mismatch"
# The final clipping width covers all eight glyphs of the neofetch command.
svg_ns = "{http://www.w3.org/2000/svg}"
type_clip = root.find(f".//{svg_ns}clipPath[@id='typeNeofetch']/{svg_ns}rect/{svg_ns}animate")
assert type_clip is not None, "SMIL typing animation missing"
assert float(type_clip.attrib["values"].split(";")[-1]) >= 76, "Last typed character gets clipped"
workspace_clip = root.find(f".//{svg_ns}clipPath[@id='typeWorkspace']/{svg_ns}rect/{svg_ns}animate")
assert workspace_clip is not None, "Missing animated workspace command"
for label, animation, command in (
    ("neofetch", type_clip, "neofetch"),
    ("workspace", workspace_clip, "ls -l ~/workspace"),
):
    widths = [float(part) for part in animation.attrib["values"].split(";")]
    assert len(widths) == len(command) + 1, f"Invalid character count: {label}"
    assert widths == sorted(widths), f"Reversed animation: {label}"
    assert widths[-1] >= len(command) * 9.03, f"Truncated command: {label}"
    assert animation.attrib["fill"] == "freeze", f"Animation must retain final state: {label}"
for stage in ("show-profile", "show-list-prompt", "show-list-output", "show-final-prompt"):
    assert f'class="{stage}' in svg, f"Missing timed stage: {stage}"
assert "prefers-reduced-motion:reduce" in svg, "Reduced-motion style missing"

# The icon is constructed from vector geometry for consistent GitHub scaling.
icon_group = [group for group in root.findall(f".//{svg_ns}g") if group.attrib.get("aria-label") == "XFCE terminal application icon"]
assert len(icon_group) == 1, "XFCE terminal application icon missing"
assert 'class="cursor"' in svg, "Shell cursor is missing"
assert "ls -l ~/workspace" in svg, "Long-format directory listing is missing"
for _date, directory in DIRECTORIES:
    assert directory in svg, f"Missing directory: {directory}"
assert f"total {len(DIRECTORIES) * 4}" in svg, "Incorrect listing block count"
assert svg.count("<script") == 0, "Script elements detected"
assert svg.count("<foreignObject") == 0, "Foreign objects detected"
assert re.search(r'(?:href|src)=["\']https?://', svg) is None, "External resource detected"

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for relative in re.findall(r'src="([^"]+)"', readme):
    assert (ROOT / relative).exists(), f"Missing README asset: {relative}"
# Both profile CTA graphics are compact and share the same viewBox.
assert CTA_OUTPUT_PATH.read_text(encoding="utf-8") == build_cta(), "Regenerate CTA from scripts/make_cta.py"
for asset in ("shellfolio-cta-arrows-v3.svg", "source-button.svg"):
    graphic = ET.parse(ROOT / "assets" / asset).getroot()
    assert graphic.attrib.get("viewBox") == "0 0 296 62", f"Misaligned CTA: {asset}"
    assert graphic.attrib.get("width") == "296", f"Inconsistent width: {asset}"
    assert graphic.attrib.get("height") == "62", f"Inconsistent height: {asset}"
    assert len(graphic.findall(f"{svg_ns}path")) >= 2, f"Missing accent or arrow in {asset}"

cta = ET.parse(CTA_OUTPUT_PATH).getroot()
source = ET.parse(ROOT / "assets" / "source-button.svg").getroot()
pink = source.findall(f"{svg_ns}path")[-1]
up = cta.find(f"{svg_ns}path[@id='terminal-up-arrow']")
right = cta.find(f"{svg_ns}path[@id='button-open-arrow']")
assert up is not None and right is not None, "The two CTA arrows are required"
assert up.attrib["d"] == pink.attrib["d"], "Up arrow must match the pink arrow geometry"
assert up.attrib["stroke-width"] == pink.attrib["stroke-width"] == "2.3"
assert up.attrib["transform"] == "rotate(-90 269 31)", "Main arrow must point up"
assert up.attrib["stroke"] == "#72df91", "Main arrow should be green"
assert right.attrib["d"] == "M158 42h14m-5-5 5 5-5 5", "Small arrow geometry changed"
assert right.attrib.get("transform") is None, "Small arrow must point right"
assert right.attrib["stroke-width"] == "1.7"
assert right.attrib["stroke"] == "#e5eaf0", "Small arrow must be white"
assert [el.text for el in cta.findall(f"{svg_ns}text")] == [
    "Click terminal above", "OR CLICK HERE TO OPEN"
], "Unexpected button captions"

assert "ShellFolio/?run=launch" in readme, "The public site must run its virtual launcher"

# The reusable profile snippet must link the animated illustration itself.
setup = (ROOT / "docs" / "PROFILE-SETUP.md").read_text(encoding="utf-8")
assert (
    '<a href="PORTFOLIO_URL"><img\n'
    '    src="https://raw.githubusercontent.com/GITHUB_USERNAME/GENERATOR_REPO/main/assets/terminal.svg"'
) in setup, "Profile SVG must be clickable"
for required in (
    "GITHUB_USERNAME",
    "GENERATOR_REPO",
    "PORTFOLIO_URL",
    "assets/shellfolio-cta-arrows-v2.svg",
    "assets/source-button.svg",
):
    assert required in setup, f"Missing template placeholder or button: {required}"

print("validated vector logo, GTK chrome, Unix listing, aligned links, and README")
