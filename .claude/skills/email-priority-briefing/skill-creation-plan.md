# Skill Creation Plan:email-priority-briefing

## Skill Overview
- **Skill name:** monthly-email-priority-briefing
- **Purpose:** Act as an executive assistant that reviews a month of Gmail activity and produces one prioritized HTML briefing of the emails that actually need the user's attention.
- **Goal:** Given the user's Gmail MCP connector, review all emails from the previous full calendar month, filter to those requiring an action or response, rank the top 20 by urgency, and output a single HTML document sectioned by priority tier.
- **Primary use case:** Once a month, the user invokes this skill with no input file required; it pulls the previous month's emails via Gmail MCP and returns a ready-to-read HTML priority briefing.

## Selected Output Deliverables
1. **README** — explains how to use the skill and what the monthly briefing contains.
2. **Skill Definition (SKILL.md)** — the finalized 8-section skill file that drives the monthly briefing.
3. **Skill Creation Plan** — this document, approved before build.
4. **Validation Summary** — gap-tracking record across the validation pass run on this package.

## Expert Roles Required
- **Skill Architect** — owns overall scope: one skill, one task (monthly triage + briefing), nothing broader.
- **Prompt Engineer** — writes Role/Goal/Context/Constraints/Guidelines/Guardrails from the already-resolved structured prompt.
- **Information Architect** — decides SKILL.md vs. references vs. templates placement for email-triage domain knowledge.
- **Domain Analyst (Inbox Triage)** — distills email-prioritization expertise into the reference files.
- **Template Designer** — defines the single HTML briefing output structure.
- **QA/Validation Reviewer** — builds and runs the validation framework against the briefing's quality bar.
- **Technical Writer** — keeps every file jargon-free and readable by a one-year-experience professional.

## Knowledge Base Captured
Seven reference files created in `references/`:
- `concept-overview.md` — what the monthly priority briefing is and the inbox-overload problem it solves.
- `key-skills.md` — 6 competencies needed (triage judgment, prioritization, Gmail data reading, summarization, HTML discipline, privacy/injection awareness).
- `critical-considerations.md` — strategic factors: inclusion filter, safety of untrusted email content, success definition.
- `best-practices.md` — anchoring inclusion to one test, ranking by urgency, fixed monthly scope, tier sectioning.
- `common-pitfalls.md` — over-inclusion, wrong ranking axis, scope drift, exceeding the cap, following embedded instructions.
- `jira-implementation.md` — documents that Jira mapping does not apply to this read-only briefing, and when it would.
- `validations.md` — the 7-dimension quality framework applied specifically to the monthly HTML briefing.

## Timeline & Phases
- **Phase A — Skill Definition & Templates:** SKILL.md and the single HTML-briefing output template built directly from the already-resolved structured prompt and the knowledge base above.
- **Phase B — Quality Assurance:** Validation framework applied to every deliverable, iterated until gaps are resolved.
- **Total duration:** Single-session build — scope was fully resolved in advance via the structured prompt this skill is built from.

## Success Criteria
- Knowledge base complete (7 files, on-topic for email triage) ✓
- This plan approved before SKILL.md and templates are finalized
- SKILL.md contains all 8 required sections, referencing templates and validations.md only, with zero inline output schemas
- Exactly one numbered template exists for the skill's one output deliverable (the HTML briefing)
- Validation pass completed against `references/validations.md` with no unresolved gaps
- Package is deployable as-is for the user's next monthly run
