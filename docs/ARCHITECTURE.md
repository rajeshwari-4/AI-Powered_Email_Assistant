# Architecture — AI Email Assistant

## Overview
The AI Email Assistant is a single Claude Skill, `email-priority-briefing`, that turns a window of Gmail inbox activity into one prioritized HTML briefing plus a spoken-audio companion, with an optional, explicitly-gated Gmail-draft step on top. There is no separate backend, database, or server — the "system" is the skill definition, one deterministic Python helper for text-to-speech, and the Gmail MCP connector already authorized in Claude.

## Components

| Component | Location | Role |
|---|---|---|
| Skill definition | `.claude/skills/email-priority-briefing/SKILL.md` | Role, Goal, Constraints, Guidelines, Guardrails, Output Format — the behavioral contract for every run |
| Reference knowledge | `.claude/skills/email-priority-briefing/references/*.md` | Domain knowledge the skill draws on: inclusion test, urgency ranking, pitfalls, quality checklist |
| Output template | `.claude/skills/email-priority-briefing/templates/1-priority-briefing-template.md` | The exact HTML structure every briefing must match |
| Audio helper | `.claude/skills/email-priority-briefing/scripts/generate_audio_summary.py` | Deterministic script: narration text → `.mp3` via gTTS, filed into `briefings/<cadence>/<label>/` alongside the HTML briefing |
| Gmail MCP connector | External (installed/authorized in Claude, not part of this repo) | Read access (search/get threads) and draft-creation access (never send) |
| Claude (the model) | Runtime | Applies the inclusion test, ranks by urgency, writes summaries and the narration script, and drives the consent gates |

## End-to-end flow

1. **Invocation** — user asks for a briefing/digest/summary; no input file required.
2. **Cadence gate** — the skill asks Daily / Weekly / Monthly before touching Gmail. This is asked every run, never assumed, never skipped.
3. **Window computation** — the chosen cadence is converted into exactly one previous full period (yesterday / last Mon–Sun / last calendar month) — never a rolling window, never overlapping or skipping a period versus the prior run of the same cadence.
4. **Data pull** — the Gmail MCP connector searches threads within that window (`in:inbox after:… before:…`), paginating as needed.
5. **Inclusion filter** — each email is tested against one rule: does it require an action or response (a request, a deadline, a direct question, an unresolved thread)? Unread status or sender identity alone never qualifies an email.
6. **Ranking & tiering** — qualifying emails are ranked by urgency and sectioned into tiers (Urgent / Needs Response / FYI), most time-sensitive first, capped at the top 20.
7. **Briefing generation** — a single self-contained HTML document is produced, matching the template exactly; empty tiers are omitted rather than shown blank.
8. **Audio generation** — Claude writes a short spoken-style narration paraphrasing the same tiered content (never a verbatim read of raw email bodies), then calls `generate_audio_summary.py` to synthesize it to `.mp3` via gTTS and file it, with a copy of the HTML briefing, under `briefings/<cadence>/<label>/`. If this step fails (e.g. no internet access), the HTML briefing is still delivered — audio never blocks the primary deliverable.
9. **Draft-consent gate** — after the briefing is shown, the skill asks which tier(s), if any, should get Gmail drafts. Silence is not consent.
10. **Drafting** — for the chosen tier(s), a draft is created only where a real, human, reply-capable correspondent exists (via `create_draft`, never `send`). Automated/no-reply senders are flagged to the user instead of force-drafted; FYI-tier items are never drafted regardless of selection. Each draft is checked against the live thread first, in case the situation moved on since the reporting window closed.
11. **Report back** — the user is told exactly which drafts were created, for which email/tier, where to find them, and that nothing was sent.

## Safety model
- **Content is data, never instructions.** Email subject/body text is summarized, never executed — this is the primary defense against prompt injection embedded in inbox content.
- **Two independent consent gates.** Cadence must be chosen before any data is pulled; tier-for-drafting must be chosen before any draft is created. Neither is inferred from the other.
- **Send capability is never invoked.** The connector's draft-creation path is the only write path this skill uses.
- **Personal output stays local and untracked.** `briefings/` holds real inbox content (HTML + audio) and is excluded from version control via `.gitignore` — it is never committed, regardless of where the project's code is hosted.

## Directory map
```
.claude/skills/email-priority-briefing/
├── SKILL.md                 # the contract described above
├── README.md                 # human-facing usage guide
├── references/                # domain knowledge (why the skill behaves this way)
├── templates/                  # the one HTML output structure
├── examples/                    # saved sample runs, one per cadence
└── scripts/
    └── generate_audio_summary.py  # narration text -> .mp3, filed by cadence/label
docs/
├── ARCHITECTURE.md            # this file
└── flow.gif                    # animated, step-by-step diagram of the flow above
briefings/                        # gitignored — real per-run output, not project code
├── daily/<date>/
├── weekly/<date>_to_<date>/
└── monthly/<Month Year>/
    ├── briefing.html
    ├── summary.mp3
    └── narration.txt
```

## See also
- [flow.gif](flow.gif) for the animated, step-by-step visual version of the flow above.
- `.claude/skills/email-priority-briefing/references/critical-considerations.md` for the strategic tradeoffs (inclusion-filter strictness, drafting-consent risk).
