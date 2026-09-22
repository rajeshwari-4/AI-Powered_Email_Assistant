# Template 1: Priority Briefing (HTML)

## Purpose
The single output artifact this skill produces each run: one self-contained HTML document that lets the user see, in under a minute, which emails from the chosen reporting window (Daily, Weekly, or Monthly) need their attention.

## Overall Structure
```html
<h1>Email Priority Briefing — {Period Label}</h1>
<p>{count} emails required action out of {total reviewed} reviewed.</p>

<h2>Urgent</h2>
<ul>
  <li><strong>{Sender}</strong> — {Subject}: {1-2 sentence factual summary, including deadline if stated}</li>
</ul>

<h2>Needs Response</h2>
<ul>
  <li><strong>{Sender}</strong> — {Subject}: {1-2 sentence factual summary}</li>
</ul>

<h2>FYI</h2>
<ul>
  <li><strong>{Sender}</strong> — {Subject}: {1-2 sentence factual summary}</li>
</ul>
```

## Each Section Should Contain
- **Title line:** the period the briefing covers — a date (Daily), a date range (Weekly, e.g. "Week of Jul 20–26, 2026"), or a month and year (Monthly) — plus a one-line count of included vs. reviewed emails.
- **Tier sections (`<h2>`):** exactly the tiers in use (e.g. Urgent, Needs Response, FYI) — omit a tier entirely if it has zero qualifying emails, rather than showing an empty header.
- **Bullets within a tier:** ordered most-to-least urgent; each bullet is one email — sender, subject, and a 1-2 sentence factual summary (core ask + deadline if any).
- **Total items across all tiers:** capped at 20, prioritized — if more than 20 qualify, keep the 20 highest-priority and drop the rest.

## Quality Standards
- Valid, self-contained HTML — no external stylesheets or scripts required to read it.
- No email is included unless it met the action/response inclusion test from `references/best-practices.md`.
- Every summary is traceable to real content in the source email — nothing invented.
- Tier and bullet order strictly follows urgency, not sender or arrival time.

## Note on Drafting
This template covers only the HTML briefing itself. Gmail draft creation is a separate step that happens after this document is shown to the user, and only for the tier(s) they explicitly ask to have drafted — it is never part of this template's output and never happens by default.
