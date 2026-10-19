"""Regression checks for unusable narration anchors and generated episode subtitles."""
import ast
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
source = ast.parse((ROOT / "tools/build.py").read_text(encoding="utf-8"))
needed = {"wide", "split_cues", "wrap2", "fmt", "seg_cues"}
body = [n for n in source.body if isinstance(n, ast.FunctionDef) and n.name in needed
        or isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "CJK" for t in n.targets)]
ns = {"re": re}
exec(compile(ast.Module(body=body, type_ignores=[]), "subtitle-functions", "exec"), ns)

class SubtitleTests(unittest.TestCase):
    def check_segment(self, words):
        text = "First sentence. Second sentence. A final sentence."
        cues = ns["seg_cues"](text, {"start": 10., "end": 19., "dur": 9., "words": words})
        self.assertGreater(len(cues), 1)
        self.assertEqual(cues[0][0], 10.)
        self.assertEqual(cues[-1][1], 19.)
        for i, (start, end, cue) in enumerate(cues):
            self.assertGreater(end, start)
            if i: self.assertGreaterEqual(start, cues[i-1][1])
        self.assertEqual(" ".join(c[2].replace("\n", " ") for c in cues), text)

    def test_all_word_anchors_zero(self): self.check_segment([{"t": 0.}] * 12)
    def test_repeated_word_anchors(self): self.check_segment([{"t": x} for x in [0, 0, 0, 0, 0, 0, 3, 3, 3]])
    def test_empty_anchors(self): self.check_segment([])
    def test_ordered_anchors(self): self.check_segment([{"t": x} for x in range(9)])
    def test_empty_text(self): self.assertEqual(ns["seg_cues"]("", {"start": 0, "end": 1, "dur": 1, "words": []}), [])
    def test_episodes_one_to_three(self):
        count = 0
        for ep in ("ep01", "ep02", "ep03"):
            files = sorted((ROOT / "video" / ep / "build").glob(f"{ep}_*.srt"))
            self.assertEqual(len(files), 12)
            for file in files:
                previous = "00:00:00,000"
                for n, start, end in re.findall(r"(\d+)\s*\n(\d\d:\d\d:\d\d,\d\d\d) --> (\d\d:\d\d:\d\d,\d\d\d)", file.read_text(encoding="utf-8")):
                    self.assertGreater(end, start, f"{file.name} cue {n}")
                    self.assertGreaterEqual(start, previous, f"{file.name} cue {n} overlaps")
                    previous = end
                    count += 1
        self.assertGreater(count, 3000)

if __name__ == "__main__": unittest.main()
