# Prototype 4 — Document Distribution & Signing Tracker

**Tasks covered:** #7 (new company document packs: CI, BR, NNC1) and #10 (annual return + CDD packs).

## What it does

1. Scans `../data/documents_out.csv` for incorporation and annual-return packs awaiting signature.
2. Computes days outstanding and picks the escalation stage — 7 days (gentle) / 14 days (firm) / 21 days (final + internal escalation).
3. Drafts the stage-appropriate chaser email with Claude/GPT (template fallback without a key) into `sample_output/chasers/`.
4. At stage 3, additionally generates the internal escalation memo to the company secretary (`sample_output/secretary_escalation.txt`) suggesting phone follow-up.

## Run it

```bash
python3 run.py --today 2026-07-14
```

Demo data shows all four states: signed-and-returned, inside grace period, stage-1 chase, and (via prototype 5) stage-3 escalation.

## Human checkpoint

Chasers are drafts — the secretary approves before sending. Escalations always go to a human; the automation never phones a client.

## Edge cases handled

- Change documents are excluded here (dedicated bilingual handling in prototype 5).
- Signed documents drop out of the chase loop immediately.
- Recently sent documents sit in a grace period rather than being chased on day 1.

## Demo evidence *(links added at submission)*

- Prompt log: [`prompt_log.md`](prompt_log.md) — exported Claude Code conversation running this task's prompts on the sample data
- Screen recording of this prototype running: _link_
