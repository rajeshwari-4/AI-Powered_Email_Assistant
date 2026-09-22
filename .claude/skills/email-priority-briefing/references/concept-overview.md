# Concept Overview: Email Priority Briefing

This skill turns a period of inbox activity — a day, a week, or a month, the user's choice each run — into one short, prioritized HTML briefing. Instead of the user re-reading every email received in that window, the skill asks which cadence to use, pulls the emails via the Gmail MCP connector for the resulting previous full period, decides which ones actually require action, ranks them by urgency, and hands back a single scannable document.

The core problem this skill solves is **inbox overload without triage**: most inboxes mix true action items (a client waiting on a reply, a deadline, an unresolved thread) with noise (newsletters, receipts, automated notices). A person reviewing the raw inbox has to do the sorting themselves every time. This skill encodes that sorting logic once — what counts as important, how to rank it, how to present it — so the same quality bar applies every run, at whichever cadence the user picks, without re-explaining the criteria.

Foundational understanding required: importance here is defined narrowly as "requires an action or response from the user," not simply unread status or sender identity. Ranking is by urgency/priority, not by topic or sender. The output is always a single HTML document, capped at the top 20 items, sectioned by priority tier so the most time-sensitive items are seen first.

A second, separately-gated layer sits on top of the briefing: after showing it, the skill asks the user which tier(s) — if any — should get Gmail drafts (never sent), so genuine action items in Urgent/Needs Response can be replied to with one review-and-send instead of a from-scratch email. This drafting layer never runs unprompted and never fabricates a reply to an automated/no-reply sender.
