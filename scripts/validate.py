#!/usr/bin/env python3
"""Validate the generated SVG and README references using the Python standard library."""

from pathlib import Path
from xml.etree import ElementTree as ET
import re

ROOT = Path(__file__).resolve().parent.parent
README = (ROOT / "README.md").read_text(encoding="utf-8")
ASSETS = ROOT / "assets"
TERMINAL = ASSETS / "terminal.svg"

# Confirm the single-scene source asset exists and parses as XML.
assert TERMINAL.is_file(), "Missing generated terminal SVG"
xml = TERMINAL.read_text(encoding="utf-8")
root = ET.fromstring(xml)
assert root.tag.endswith("svg"), "Expected an SVG root element"

# Verify the home scene and the long-format listing are represented.
assert "ls -l ~/workspace" in xml, "The shell listing is absent"
for directory in ("hardware/", "embedded/", "software/", "fabrication/", "projects/"):
    assert directory in xml, f"Missing long-format directory: {directory}"
assert "<animate " in xml, "Expected an SMIL command animation"
assert "class=\"cursor\"" in xml, "Expected a visible shell cursor"

# Keep references local and ensure all README images are available.
assert xml.count("<script") == 0, "SVG script elements detected"
assert xml.count("<foreignObject") == 0, "Foreign HTML elements detected"
assert re.search(r'(?:href|src)=["\']https?://', xml) is None, "External SVG resource found"
for relative in re.findall(r'src="([^"]+)"', README):
    assert (ROOT / relative).is_file(), f"Missing README image: {relative}"

print("validated terminal SVG structure, animation and README asset references")
