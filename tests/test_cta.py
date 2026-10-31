"""Regression tests for compact CTA arrow customization (no extra packages)."""
import sys
import unittest
from dataclasses import replace
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from make_cta import Arrow, INLINE_ARROW, MAIN_ARROW, OUTPUT_PATH, build_cta, render_arrow

SVG = "{http://www.w3.org/2000/svg}"


class CtaTests(unittest.TestCase):
    def test_generated_file_matches_checked_in_asset(self):
        self.assertEqual(OUTPUT_PATH.read_text(encoding="utf-8"), build_cta())
        root = ET.fromstring(build_cta())
        self.assertEqual(root.attrib["viewBox"], "0 0 296 62")
        self.assertEqual(len(root.findall(f"{SVG}text")), 2)

    def test_green_arrow_matches_pink_size_and_orientation(self):
        root = ET.fromstring(build_cta())
        green = root.find(f"{SVG}path[@id='terminal-up-arrow']")
        pink = ET.parse(OUTPUT_PATH.parent / "source-button.svg").getroot().findall(f"{SVG}path")[-1]
        self.assertEqual(green.attrib["d"], pink.attrib["d"])
        self.assertEqual(green.attrib["stroke-width"], pink.attrib["stroke-width"])
        self.assertEqual(green.attrib["transform"], "rotate(-90 269 31)")
        self.assertEqual(green.attrib["stroke"], "#72df91")

    def test_smaller_right_arrow_is_white_and_follows_second_label(self):
        root = ET.fromstring(build_cta())
        small = root.find(f"{SVG}path[@id='button-open-arrow']")
        self.assertEqual(small.attrib["d"], "M158 42h14m-5-5 5 5-5 5")
        self.assertNotIn("transform", small.attrib)
        self.assertEqual(small.attrib["stroke"], "#e5eaf0")
        self.assertEqual(small.attrib["stroke-width"], "1.7")

    def test_each_direction_rotates_same_vector_in_place(self):
        expected = {"right": None, "down": "rotate(90 269 31)",
                    "left": "rotate(180 269 31)", "up": "rotate(-90 269 31)"}
        for direction, rotation in expected.items():
            with self.subTest(direction=direction):
                element = ET.fromstring(render_arrow(replace(MAIN_ARROW, direction=direction)))
                self.assertEqual(element.attrib.get("transform"), rotation)
                self.assertEqual(element.attrib["d"], "M259 31h20m-8-8 8 8-8 8")

    def test_length_and_color_are_configurable_without_new_markup(self):
        original = ET.fromstring(render_arrow(INLINE_ARROW))
        customized = ET.fromstring(render_arrow(replace(INLINE_ARROW,
                                                        length=18, color="#AABBCC", stroke=2)))
        self.assertEqual(customized.attrib["stroke"], "#AABBCC")
        self.assertEqual(customized.attrib["stroke-width"], "2")
        self.assertNotEqual(original.attrib["d"], customized.attrib["d"])
        self.assertEqual(customized.attrib["d"], "M156 42h18m-7-7 7 7-7 7")
        self.assertEqual(customized.attrib["id"], original.attrib["id"])

    def test_invalid_parameters_are_rejected(self):
        invalid = (
            {"direction": "diagonal"},
            {"length": 7},
            {"length": 13},
            {"length": 38},
            {"length": True},
            {"x": 1},
            {"x": 286},
            {"y": 7},
            {"stroke": 0.1},
            {"stroke": 5},
            {"stroke": float("nan")},
            {"color": "red"},
            {"color": '" onload="alert(1)'},
            {"identifier": 'x" onload="alert(1)'},
        )
        for changes in invalid:
            with self.subTest(changes=changes):
                with self.assertRaises(ValueError):
                    render_arrow(replace(MAIN_ARROW, **changes))

    def test_arrow_ids_must_not_collide(self):
        with self.assertRaises(ValueError):
            build_cta(MAIN_ARROW, replace(INLINE_ARROW, identifier=MAIN_ARROW.identifier))


if __name__ == "__main__":
    unittest.main()
