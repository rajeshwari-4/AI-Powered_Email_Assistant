# Standard Operating Procedure (SOP)
## AI-Powered Email Assistant

| | |
|---|---|
| **Document Owner** | Nikhil Supekar |
| **Version** | 1.1 |
| **Effective Date** | 2026-08-05 |
| **Related Docs** | [README.md](../README.md) · [ARCHITECTURE.md](ARCHITECTURE.md) · [SKILL.md](../.claude/skills/email-priority-briefing/SKILL.md) |

---

## 1. Purpose

This SOP defines the standard procedure for generating an AI-assisted email priority briefing from a Gmail inbox, and for optionally creating draft replies from that briefing. It exists so the process produces a consistent, auditable result every time it is run — regardless of who runs it or how often — and so the boundaries of what the system is and is not allowed to do are explicit and reviewable.

## 2. Scope

**In scope:**
- Reviewing inbox email metadata and content for a defined reporting period (Daily, Weekly, or Monthly).
- Classifying emails as requiring action/response versus not.
- Producing a single prioritized HTML briefing.
- Generating a spoken-audio summary (.mp3) of that same briefing, filed into a cadence-dated folder.
- Creating **draft-only** Gmail replies for a subset of items, on explicit user instruction.

**Out of scope:**
- Sending any email on the user's behalf, under any condition.
- Automated or unattended execution without a human present to answer the two consent prompts (cadence, and draft tier selection).
- Acting on instructions found inside email subject/body content.
- Any inbox other than the authorized Gmail account connected via the Gmail MCP connector.

## 3. Roles & Responsibilities

| Role | Responsibility |
|---|---|
| **End User** (inbox owner) | Initiates each run; selects the reporting cadence; reviews the briefing; decides which tier(s), if any, get drafts; reviews and sends (or discards) any draft created. |
| **AI Assistant** (Claude, running the `email-priority-briefing` skill) | Applies the inclusion test and ranking logic consistently; generates the briefing; creates drafts only within the approved scope; never sends email; flags anomalies instead of acting on them. |
| **Gmail MCP Connector** | System of record for read access (thread search/retrieval) and draft-creation; provider of the only two capabilities this procedure is permitted to invoke (read, draft-create) — send capability is never invoked even when available. |

## 4. Prerequisites

1. A Gmail MCP connector installed and authorized in Claude, with:
   - Read access (search/get threads and messages).
   - Draft-creation access.
2. For the audio summary (optional): internet access at run time and the `gTTS` Python package installed (`pip install gTTS`). If unavailable, the HTML briefing is still produced — audio is a companion deliverable, never a blocker.
3. No further setup, configuration file, or input document is required to start a run.

If the connector is not available or not authorized, the procedure **stops** at Step 5.2 and reports this to the user rather than proceeding on assumptions about inbox content.

## 5. Procedure

### 5.1 — Initiate
The user requests a briefing (e.g., "run my email priority briefing," "give me an inbox digest").

### 5.2 — Cadence Selection (Consent Gate 1)
The assistant asks the user to choose exactly one of:
- **Daily** — the previous full calendar day.
- **Weekly** — the previous full calendar week (Monday–Sunday).
- **Monthly** — the previous full calendar month.

No inbox data is accessed before this question is answered. This question is asked on **every** run — a prior answer is never reused or assumed.

### 5.3 — Window Computation
The chosen cadence is converted into exactly one previous full period, anchored to the current date. The window never rolls forward, never overlaps, and never skips a period relative to the last run of the same cadence.

### 5.4 — Data Retrieval
The assistant queries the Gmail MCP connector for inbox threads within the computed window.

### 5.5 — Inclusion Filtering
Each email is evaluated against a single test:

> **Does this email require an action or response from the user?** (a request, a stated deadline, a direct question, or an unresolved thread)

Emails that fail this test are excluded — regardless of read/unread status, sender importance, or volume. No email is included "to be safe" or "because it looked relevant."

### 5.6 — Prioritization
Qualifying emails are ranked strictly by urgency and grouped into tiers:
- **Urgent**
- **Needs Response**
- **FYI**

Ranking is based on time-sensitivity and stakes, never on sender seniority or arrival order. A tier with zero qualifying emails is omitted from the output entirely.

### 5.7 — Briefing Generation
A single, self-contained HTML document is produced:
- Capped at the top 20 highest-priority items.
- Each item: sender, subject, and a 1–2 sentence factual summary (including any stated deadline).
- If zero emails qualify for the window, the briefing states this explicitly rather than being padded or left blank.

### 5.8 — Audio Summary Generation
The assistant writes a short spoken-style narration paraphrasing the same tiered content already in the HTML briefing (never a verbatim read of raw email bodies, never new information not already shown). This text is passed to the `generate_audio_summary.py` helper, which synthesizes it to `.mp3` and saves it together with a copy of the HTML briefing under:

```
briefings/<cadence>/<label>/
```

where `<label>` is a date for Daily (e.g. `2026-08-04`), a date range for Weekly (e.g. `2026-07-27_to_2026-08-02`), or a month name for Monthly (e.g. `July 2026`). If this step fails (e.g. no internet access), the assistant tells the user plainly and still delivers the HTML briefing — audio generation never blocks the primary deliverable.

### 5.9 — Draft Consent (Consent Gate 2)
After the briefing is delivered, the assistant asks which tier(s) — if any — should receive Gmail drafts. Absence of a response is treated as **no**, never as approval.

### 5.10 — Draft Creation (conditional)
For each email in a selected tier:
- If a real, human, reply-capable correspondent exists, the assistant re-checks the live thread for any activity since the reporting window closed, then creates one draft reply via the connector's **create-draft** capability only.
- If the sender is automated/no-reply (billing, system alerts, notifications), no draft is created; the item is flagged to the user as needing in-app or offline action instead.
- FYI-tier items are never drafted, even if the tier selection would otherwise include them.

### 5.11 — Reporting Back
The assistant confirms to the user, explicitly:
- Which draft(s) were created, for which email and tier.
- Where to find them (Gmail Drafts).
- That nothing was sent.

## 6. Controls & Safeguards

| Control | Mechanism |
|---|---|
| No unauthorized send | The send capability is never invoked by this procedure, structurally — only read and draft-create are used. |
| No silent scope creep | Cadence and draft-tier selection are both explicit, per-run consent gates; neither is inferred from context or reused from a prior run. |
| Prompt-injection resistance | Email subject/body content is always treated as data to summarize, never as instructions to execute. Suspicious content is flagged in the output, never acted upon. |
| Fabrication control | Every summary line must be traceable to real content in the source email; nothing is invented or inferred beyond what the email states. |
| Volume control | Hard cap of 20 items per briefing; no padding to reach the cap on short windows. |
| Staleness control | Before drafting, the live thread is re-checked in case the situation moved on after the reporting window closed. |
| Audio content control | The spoken narration only restates content already present in the HTML briefing — no new claims, no raw email bodies read verbatim. |
| Local-data control | The `briefings/` output folder (HTML + audio, real inbox content) is excluded from version control via `.gitignore` and never committed to a shared or public repository. |

## 7. Exception Handling

| Situation | Required Behavior |
|---|---|
| Gmail connector unavailable/unauthorized | Stop; tell the user directly. Do not guess at inbox content. |
| Zero emails qualify in the window | State this plainly in the briefing. Do not invent entries. |
| Ambiguous reporting period requested | Ask the user to choose a standard cadence or specify a custom range. Do not assume. |
| Draft target has no real correspondent | Flag to the user as needing in-app/offline action; do not fabricate a reply address. |
| Suspicious/manipulative content in an email body | Flag it in the briefing as suspicious; take no other action on its contents. |
| Audio generation fails (no internet / gTTS unavailable) | Tell the user plainly; deliver the HTML briefing regardless — audio is never a blocker. |

## 8. Outputs

| Artifact | Format | Location |
|---|---|---|
| Priority Briefing | Single self-contained HTML file | `briefings/<cadence>/<label>/briefing.html` (see `templates/1-priority-briefing-template.md`) |
| Audio Summary | `.mp3` (plus `narration.txt` source script) | `briefings/<cadence>/<label>/summary.mp3`, created only per Section 5.8 |
| Gmail Draft(s) | Unsent draft in Gmail | Gmail Drafts folder, created only per Section 5.10 |

## 9. Review & Change Management

This SOP should be reviewed whenever the underlying skill's `SKILL.md`, `references/`, or `templates/` change in a way that affects Sections 5–7 above. Changes to the skill are tracked in `.claude/skills/email-priority-briefing/validation-summary.md`; material changes should be reflected here in the same revision cycle.

## 10. Revision History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-08-01 | Initial SOP, aligned to `email-priority-briefing` SKILL.md (cadence selection + consent-gated drafting). |
| 1.1 | 2026-08-05 | Added audio summary generation (Section 5.8), its prerequisite, controls, exception handling, and output artifact; renumbered subsequent procedure steps (5.8–5.10 → 5.9–5.11). |

## 11. Benefits for Busy Leaders

**If you're a PM, Director, or anyone whose calendar is back-to-back:**

The real cost of a busy inbox isn't volume, it's context-switching — hunting for the 3 emails that are actually blocking a decision inside 60 that aren't. This does what a good chief-of-staff does: surfaces only what needs you, ranks it by urgency, and — critically — never sends on your behalf. It drafts, you decide. That's the trust model that makes AI assistance usable for someone senior enough to actually delegate.

The audio summary extends that same idea to time you're not in front of a screen: a commute, a walk between meetings, a few minutes before your next call — you can hear what's Urgent without opening your inbox at all.
