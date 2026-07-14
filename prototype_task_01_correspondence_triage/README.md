# Prototype 1 — Incoming Correspondence Triage

**Task covered:** #1 — categorize, log and file all incoming correspondence; notify clients via email, WeChat and WhatsApp.

## What it does

1. Reads every letter/parcel note in `../data/correspondence/` (6 realistic samples: IRD tax notice, bank statement, CR reminder, junk mail, court summons, parcel with share certificates).
2. Classifies each item with Claude/GPT using the prompt in `prompts/correspondence_classifier.md` — category, urgency, deadline extraction, notify-or-not decision.
3. Appends every item to `sample_output/correspondence_log.csv` (the digital mailroom log).
4. For items needing client attention, drafts **three channel versions** of the notification (email / WhatsApp / WeChat, Chinese where the client prefers it) using `prompts/client_notification.md`.

## Run it

```bash
export ANTHROPIC_API_KEY=sk-...   # or OPENAI_API_KEY; omit for template mode
python3 run.py --today 2026-07-14
```

Without a key it falls back to clearly-labelled rule-based templates, so the end-to-end flow always demonstrates.

## Human checkpoint

No notification is auto-sent. Drafts land in `sample_output/notifications/` for a staff member to review — urgent legal items are flagged `!!` for same-day handling.

## Edge cases handled

- Court summons → forced `urgent`, client always notified, "consult your legal adviser" language, never legal advice.
- Physical valuables (chops, share certificates) → notification must confirm secure storage.
- Marketing junk → logged but never forwarded, keeping client channels high-signal.
- Unrecognized items → routed to manual review rather than guessed.

## Demo evidence *(links added at submission)*

- Live prompt thread (Claude / ChatGPT shared conversation): _link_
- Screen recording of this prototype running: _link_
