#!/usr/bin/env python3
"""Deterministic helper: turns a spoken-style narration script into an .mp3
and files it under briefings/<cadence>/<label>/, alongside a copy of the
HTML briefing and the raw narration text (for review/debugging).

This script does not decide *what* to say — the calling skill run writes the
narration text (a plain-language paraphrase of the Urgent/Needs Response/FYI
tiers, never raw email bodies) and passes it in. This script only handles the
deterministic parts: folder naming per cadence, text-to-speech, and file
placement.

Requires internet access at run time (uses Google Translate's TTS endpoint
via the `gTTS` package: pip install gTTS).

Usage:
    python generate_audio_summary.py --cadence monthly --label "July 2026" \\
        --text-file narration.txt [--html-source briefing.html] \\
        [--base-dir briefings]
"""
import argparse
import shutil
import sys
from pathlib import Path

CADENCES = ("daily", "weekly", "monthly")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cadence", required=True, choices=CADENCES,
                         help="Which reporting cadence this run used.")
    parser.add_argument("--label", required=True,
                         help='Folder name for this run: a date for daily '
                              '(e.g. "2026-08-04"), a date range for weekly '
                              '(e.g. "2026-07-27_to_2026-08-02"), or a month '
                              'name for monthly (e.g. "July 2026").')
    parser.add_argument("--text-file", required=True,
                         help="Path to a text file containing the spoken-style "
                              "narration script to synthesize.")
    parser.add_argument("--html-source",
                         help="Optional path to the HTML briefing for this run; "
                              "if given, it is copied alongside the audio file.")
    parser.add_argument("--base-dir", default="briefings",
                         help='Root output folder (default: "briefings", '
                              "created relative to the current working "
                              "directory — invoke this from the project root).")
    parser.add_argument("--lang", default="en", help="gTTS language code (default: en).")
    args = parser.parse_args()

    narration_path = Path(args.text_file)
    if not narration_path.is_file():
        print(f"error: --text-file not found: {narration_path}", file=sys.stderr)
        sys.exit(1)
    text = narration_path.read_text(encoding="utf-8").strip()
    if not text:
        print("error: narration text is empty", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(args.base_dir) / args.cadence / args.label
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        from gtts import gTTS
    except ImportError:
        print("error: gTTS is not installed. Run: pip install gTTS", file=sys.stderr)
        sys.exit(1)

    mp3_path = out_dir / "summary.mp3"
    try:
        gTTS(text=text, lang=args.lang).save(str(mp3_path))
    except Exception as exc:
        print(f"error: text-to-speech failed ({exc}). gTTS requires internet "
              "access to Google's TTS endpoint at run time.", file=sys.stderr)
        sys.exit(1)

    narration_out = out_dir / "narration.txt"
    narration_out.write_text(text, encoding="utf-8")

    if args.html_source:
        html_src = Path(args.html_source)
        if html_src.is_file():
            shutil.copy2(html_src, out_dir / "briefing.html")
        else:
            print(f"warning: --html-source not found, skipped: {html_src}", file=sys.stderr)

    print(f"Saved: {mp3_path}")


if __name__ == "__main__":
    main()
