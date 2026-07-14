# Prototype 3 — Master Filing Log with Computed Deadlines

**Tasks covered:** #3 (master filing log) and #8 (annual return deadline tracking).

## What it does

1. **Computes** each company's statutory obligations from first principles rather than trusting manual entry:
   - NAR1 annual return — incorporation anniversary + 42 days (CO s.662)
   - 56AB employer's return — for payroll clients, due 2 May
   - PTR profits tax return — block extension date by year-end code
2. Cross-references `../data/filings.csv` so already-filed items don't alert, and merges one-off items (NOAs, director ITRs).
3. Writes the consolidated `sample_output/master_filing_log.csv` (24 obligations across 10 companies in the demo) and prints an **alert digest** of everything overdue or due within 30 days.
4. Emits the daily digest email for the company secretary (`sample_output/alert_digest_email.txt`).

## Run it

```bash
python3 run.py --today 2026-07-14
```

## Production deployment

The same logic ships as Google Apps Script in `../shared/apps_script/reminder_engine.gs` — bind to the master tracker Sheet, add a daily trigger, and alerts send via MailApp with zero infrastructure.

## Human checkpoint

The secretary validates computed deadlines the first time each company enters the log; after that the engine only surfaces exceptions.

## Edge cases handled

- Filed obligations are excluded from alerts (no noise).
- Overdue items stay in the digest until resolved — they never age out.
- Companies without payroll/tax service don't generate 56AB/PTR noise.

## Demo evidence *(links added at submission)*

- Live Google Sheet (view-only) with the Apps Script reminder engine: _link_
- Screen recording of this prototype running: _link_

*(No prompt log for this task by design — deadline computation is deterministic code; AI sits upstream and downstream, see the design.)*
