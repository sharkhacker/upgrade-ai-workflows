# Upgrade AI — AI Workflow Consultant Assessment

Redesign of 12 manual admin workflows for a Hong Kong company secretarial / accounting firm — **all 12 written designs** and **6 working prototypes** (assessment asked for 3+).

**Author:** Shrikant — AI & Automation Engineer. For the last 3–4 years I've been building AI-assisted workflow automation for internal teams (finance, GTM, HR, customer support), which is exactly the shape of this problem: repetitive intake, deadline tracking, document generation, and follow-up loops where AI removes the reading and drafting while humans keep the judgment.

## The one design idea that runs through everything

Six of the twelve tasks (3, 7, 8, 10, 11, 12) are the same machine: *a register + a clock + escalating reminders + human escalation*. I built that machine once — [`shared/engine.py`](shared/engine.py) for the demos, [`shared/apps_script/reminder_engine.gs`](shared/apps_script/reminder_engine.gs) for production on Google Sheets — and pointed it at different registers. One place to tune thresholds, one pattern for staff to learn.

The second principle: **AI drafts, humans decide, data stays out of the model's hands.** Fees come from a fee schedule, deadlines from date math, payment status from humans. Claude/GPT do what they're best at — reading messy documents, drafting personalized bilingual messages — and never invent facts.

## Task index

| # | Task | Design | Prototype |
|---|---|---|---|
| 1 | Incoming correspondence handling | [design](docs/01_incoming_correspondence.md) | [P1 — triage + multi-channel notify](prototypes/01_correspondence_triage/) |
| 2 | Statutory filing notifications | [design](docs/02_statutory_filing_notifications.md) | [P2 — deadline + fee emails, NOA alerts](prototypes/02_filing_notifications/) |
| 3 | Master filing log | [design](docs/03_master_filing_log.md) | [P3 — computed deadlines + digest](prototypes/03_master_filing_log/) |
| 4 | Company incorporation support | [design](docs/04_company_incorporation_support.md) | design only |
| 5 | CDD search | [design](docs/05_cdd_search.md) | design only |
| 6 | Incorporation document preparation | [design](docs/06_incorporation_document_prep.md) | design only (sample prompt included) |
| 7 | New company doc distribution & tracking | [design](docs/07_new_company_doc_distribution.md) | [P4 — signing tracker + chasers](prototypes/04_distribution_tracking/) |
| 8 | Annual return deadline tracking | [design](docs/08_annual_return_deadline_tracking.md) | covered by P3 |
| 9 | Annual return preparation | [design](docs/09_annual_return_preparation.md) | design only (roll-forward prompt included) |
| 10 | Annual return distribution & tracking | [design](docs/10_annual_return_distribution.md) | covered by P4 |
| 11 | Change-of-document tracking 已提供給客戶未簽回的變更文件 | [design](docs/11_change_doc_tracking.md) | [P5 — bilingual EN/中文 reminders](prototypes/05_change_doc_reminders/) |
| 12 | Invoicing & payment tracking | [design](docs/12_invoicing_payment_tracking.md) | [P6 — invoicing + dunning](prototypes/06_invoicing_tracking/) |

## Running the prototypes

Python 3.10+, standard library only — nothing to install.

```bash
# with live AI drafting (Claude preferred, GPT also supported)
export ANTHROPIC_API_KEY=sk-...        # or OPENAI_API_KEY

# run everything against the fixed demo date
for p in prototypes/0*/run.py; do python3 "$p" --today 2026-07-14; done
```

Without an API key every prototype still runs end-to-end using clearly labelled `[template mode]` fallbacks — the same graceful-degradation pattern I use in production automations. Generated emails, logs and registers land in [`outputs/`](outputs/) (sample outputs are committed so you can browse without running anything).

## Repo map

```
data/        realistic dummy dataset: 10 HK companies, filings, sample letters,
             documents-out register, invoices, fee schedule (no real client data)
shared/      ai.py (Claude/GPT wrapper) · engine.py (reminder engine) ·
             prompts/ (the 5 core prompts) · apps_script/ (production deployment)
prototypes/  6 runnable demos, one folder per prototype with its own README
docs/        the 12 written workflow designs
outputs/     sample generated artifacts from a run on 2026-07-14
```

## Tools used and why

- **Claude** — primary: document classification, extraction, bilingual (EN/繁體中文) drafting, template filling.
- **GPT (ChatGPT)** — supported as an alternate provider in the same wrapper; used for comparison during prompt development.
- **Google Sheets + Apps Script** — master registers and the daily reminder trigger; free, auditable, and where the firm's staff already live.
- **Python (stdlib)** — demo harness so evaluators can run everything with zero setup.
- **WhatsApp Business API / WeCom** — production notification channels (mocked as drafts here; template-message approval is a noted dependency).
