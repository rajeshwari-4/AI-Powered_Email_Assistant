# Project Goal

Build an AI email assistant, implemented as the `email-priority-briefing` Claude Skill, that turns a period of Gmail inbox activity into a single prioritized briefing so the user never has to re-triage a raw inbox by hand.

## What it does
- Reviews inbox activity over a user-chosen cadence — Daily, Weekly, or Monthly (asked fresh every run, never assumed) — for exactly one previous full period.
- Applies one inclusion test: only include emails that require an action or response (a request, a deadline, a direct question, an unresolved thread) — never unread status or sender identity alone.
- Ranks qualifying emails by urgency, sections them into tiers (Urgent / Needs Response / FYI), and outputs a single capped, self-contained HTML briefing.
- Optionally, after the briefing is shown and only on explicit per-tier consent, creates Gmail drafts (never sent) replying to items that have a real human correspondent — automated/no-reply senders are flagged instead, never drafted to.

## Core problem solved
Inbox overload without triage: real action items (a client waiting on a reply, a deadline, an unresolved thread) get buried in noise (newsletters, receipts, automated notices). This assistant encodes the sorting/ranking/drafting-consent logic once so the same quality bar applies at every cadence, every run.

## Non-goals
- Not a send-capable assistant — drafting is strictly draft-only, gated behind explicit user choice.
- Not a rolling-window digest — always exactly one previous full period per cadence, no gaps or overlaps.
- Not a Jira/task-tracking integration.
