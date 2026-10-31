"""Regression tests for the GitHub profile SVG scheduler."""
import sys
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from timing import build_timeline, clip_animation


class TimelineTests(unittest.TestCase):
    def test_prompts_and_typing_have_independent_timing(self):
        run = build_timeline(("neofetch", "ls -l ~/workspace"))
        self.assertEqual(len(run.cues), 2)
        first, second = run.cues
        self.assertLess(first.typing_at_ms, first.typing_done_ms)
        self.assertLess(first.typing_done_ms, first.result_at_ms)
        self.assertGreater(second.prompt_at_ms, first.result_at_ms)
        self.assertLess(second.prompt_at_ms, second.typing_at_ms)
        self.assertGreaterEqual(second.typing_at_ms - first.result_at_ms, 200)
        self.assertLess(second.typing_at_ms - first.result_at_ms, 300)
        self.assertLess(run.final_prompt_at_ms - second.result_at_ms, 150)

    def test_typing_never_reverses_or_clips_last_character(self):
        command = "ls -l ~/workspace"
        animation = ET.fromstring(clip_animation(command, 100, 900))
        widths = [float(n) for n in animation.attrib["values"].split(";")]
        self.assertEqual(len(widths), len(command) + 1)
        self.assertEqual(widths, sorted(widths))
        self.assertGreater(widths[-1], len(command) * 9)
        self.assertEqual(animation.attrib["fill"], "freeze")

    def test_invalid_commands_rejected(self):
        for commands in ((), ("",), ("neofetch", "  ")):
            with self.subTest(commands=commands):
                with self.assertRaises(ValueError):
                    build_timeline(commands)


if __name__ == "__main__":
    unittest.main()
