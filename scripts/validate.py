#!/usr/bin/env python3
"""Offline validation of Engineering OS SVG assets and Markdown links (stdlib only)."""
from pathlib import Path
from xml.etree import ElementTree as ET
import re

ROOT = Path(__file__).resolve().parent.parent
readme = (ROOT / "README.md").read_text(encoding="utf-8")
assets = ROOT / "assets"
svg_files = sorted(assets.glob("*.svg"))
assert len(svg_files) >= 13, f"Only {len(svg_files)} SVG assets found"
for p in svg_files:
    src = p.read_text(encoding="utf-8")
    ET.fromstring(src)
    assert src.count("<script") == 0 and src.count("<foreignObject") == 0, p
    # SVG XML requires its namespace URI; embedded resource references stay local.
    assert re.search(r'(?:href|src)=["\']https?://', src) is None, p
for relative in re.findall(r'src="([^"]+)"', readme):
    assert (ROOT / relative).is_file(), f"Missing image: {relative}"
assert readme.count("<details>") == readme.count("</details>")
print(f"validated {len(svg_files)} SVGs, README images and disclosure elements")
