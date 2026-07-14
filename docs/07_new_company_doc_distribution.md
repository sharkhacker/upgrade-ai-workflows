# Task 7 — New Company Document Distribution & Tracking

> Send out all new CI, BR, NNC1 forms, etc. to the client for record and signing; track signing status and remind the company secretary if documents haven't been signed and returned.

**Prototype: yes — [`prototypes/04_distribution_tracking/`](../prototypes/04_distribution_tracking/)** (shared with task 10)

## Why this design

Tasks 7, 10 and 11 are the same machine with different documents: a register of what went out, a clock, an escalating chaser, and an internal escalation. I built that machine once (`shared/engine.py` / `reminder_engine.gs`) and pointed it at three registers — in my experience consolidating "reminder-shaped" workflows into one engine is where the real maintenance savings live.

## Workflow

| Step | Actor | Detail |
|---|---|---|
| Trigger | — | Incorporation pack ready (task 6 output): CI, BR, NNC1, minutes for signing |
| 1. Dispatch | Automation + **Claude** | Cover email drafted per client (what each document is, which pages to sign, how to return); pack sent; register row created with sent date and expected signer |
| 2. Track | Automation | Daily scan computes days outstanding for everything `awaiting_signature` |
| 3. Chase | **Claude** | Stage 1 at 7 days (gentle), stage 2 at 14 (firm — states what's blocked), stage 3 at 21 (final — statutory risk, respond-by date) |
| 4. **Human checkpoint** | Staff | Chasers are drafts pending approval; returned documents are marked by a human, which stops the clock |
| 5. Escalate | Automation | Stage 3 generates the internal memo to the company secretary with full history, suggesting phone follow-up |

## Tools & why

- **Shared reminder engine** — Sheets register + Apps Script daily trigger in production; identical logic across tasks 7/10/11 means one place to tune thresholds.
- **Claude for the words, the engine for the decisions** — escalation stage is computed by date math, so tone escalation is consistent and auditable; the model only writes the message for the stage it's told.

## Output

Live dispatch register (what's out, with whom, how long), stage-appropriate chaser drafts, and secretary escalations that arrive with history attached instead of "can you chase Mr. Ng?"

## Edge cases & escalations

- **Partial returns** (2 of 3 documents back) — register tracks per document, so the chaser names exactly what's missing.
- **Grace period** — nothing is chased in the first 7 days; day-1 nagging costs goodwill.
- **Client disputes content** — reply pauses the chase clock and routes to staff.
- **Wrong signer** — register records the expected signer, so chasers address the right person, not just the mailbox.
