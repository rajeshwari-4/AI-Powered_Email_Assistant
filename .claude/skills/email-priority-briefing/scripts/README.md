# Scripts

Deterministic helper scripts — the parts of this skill that are fixed logic, not judgment calls. Triage, prioritization, and summarization stay the model's job; anything mechanical lives here instead.

- **`generate_audio_summary.py`** — takes a narration text file plus the cadence/label for the current run, synthesizes it to `.mp3` via `gTTS`, and files it (with a copy of the HTML briefing) under `briefings/<cadence>/<label>/`. Requires `pip install gTTS` and internet access at run time; if it fails, the HTML briefing is still delivered. See usage in its module docstring or `SKILL.md` Guideline 7.
