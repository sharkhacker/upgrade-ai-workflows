# Upgrade AI — AI Workflow Consultant Assessment

Redesign of 12 manual admin workflows for a Hong Kong company secretarial / accounting firm — **all 12 written designs** and **6 working prototypes** (assessment asked for 3+).

**Author:** Shrikant — AI & Automation Engineer. For the last 3–4 years I've been building AI-assisted workflow automation for internal teams (finance, GTM, HR, customer support), which is exactly the shape of this problem: repetitive intake, deadline tracking, document generation, and follow-up loops where AI removes the reading and drafting while humans keep the judgment.

## How this repo is organized

**One folder per task, named by task number.** Folders starting with `prototype_` contain a working, runnable prototype; the rest are written designs. Every task folder is self-contained:

- `README.md` — what the automation does and (for prototypes) how to run it
- `DESIGN.md` — the full workflow design: trigger, AI steps, tools, human checkpoints, output, edge cases *(in prototype folders; design-only folders have this content in their README)*
- `run.py` + `prompts/` — the automation and its AI prompts *(prototype folders)*
- `sample_output/` — committed results of a run on 2026-07-14, so you can review without running anything

Shared across tasks: [`data/`](data/) (the dummy client dataset all tasks operate on) and [`shared/`](shared/) (the reminder engine, the Claude/GPT wrapper, and the production Google Apps Script).

**Every design opens with a flow diagram** (GitHub renders them automatically). One color language throughout: **purple = AI does the work, orange = a human decides, green = the result.** If you read nothing else in a folder, the diagram tells the story.

## Task index

| # | Task | Folder | Working prototype |
|---|---|---|---|
| 1 | Incoming correspondence handling | [`prototype_task_01_correspondence_triage/`](prototype_task_01_correspondence_triage/) | ✅ triage + email/WhatsApp/WeChat drafts |
| 2 | Statutory filing notifications | [`prototype_task_02_filing_notifications/`](prototype_task_02_filing_notifications/) | ✅ deadline + fee emails, NOA payment alerts |
| 3 | Master filing log | [`prototype_task_03_master_filing_log/`](prototype_task_03_master_filing_log/) | ✅ computed deadlines + daily digest |
| 4 | Company incorporation support | [`task_04_company_incorporation_support/`](task_04_company_incorporation_support/) | design |
| 5 | CDD search | [`task_05_cdd_search/`](task_05_cdd_search/) | design |
| 6 | Incorporation document preparation | [`task_06_incorporation_document_prep/`](task_06_incorporation_document_prep/) | design + generation prompt |
| 7 | New company doc distribution & tracking | [`prototype_task_07_doc_distribution_tracking/`](prototype_task_07_doc_distribution_tracking/) | ✅ signing tracker + escalating chasers |
| 8 | Annual return deadline tracking | [`task_08_annual_return_deadline_tracking/`](task_08_annual_return_deadline_tracking/) | ✅ via task 3 prototype |
| 9 | Annual return preparation | [`task_09_annual_return_preparation/`](task_09_annual_return_preparation/) | design + roll-forward prompt |
| 10 | Annual return distribution & tracking | [`task_10_annual_return_distribution/`](task_10_annual_return_distribution/) | ✅ via task 7 prototype |
| 11 | Change-of-document tracking 已提供給客戶未簽回的變更文件 | [`prototype_task_11_change_doc_reminders/`](prototype_task_11_change_doc_reminders/) | ✅ bilingual EN/中文 reminders |
| 12 | Invoicing & payment tracking | [`prototype_task_12_invoicing_payment_tracking/`](prototype_task_12_invoicing_payment_tracking/) | ✅ invoicing + dunning sequence |

## The one design idea that runs through everything

Six of the twelve tasks (3, 7, 8, 10, 11, 12) are the same machine: *a register + a clock + escalating reminders + human escalation*. I built that machine once — [`shared/engine.py`](shared/engine.py) for the demos, [`shared/apps_script/reminder_engine.gs`](shared/apps_script/reminder_engine.gs) for production on Google Sheets — and pointed it at different registers. One place to tune thresholds, one pattern for staff to learn.

The second principle: **AI drafts, humans decide, data stays out of the model's hands.** Fees come from a fee schedule, deadlines from date math, payment status from humans. Claude/GPT do what they're best at — reading messy documents, drafting personalized bilingual messages — and never invent facts.

## Running the prototypes

Python 3.10+, standard library only — nothing to install.

```bash
# run everything against the fixed demo date
for p in prototype_task_*/run.py; do python3 "$p" --today 2026-07-14; done
```

The AI wrapper ([`shared/ai.py`](shared/ai.py)) picks the first available provider: `ANTHROPIC_API_KEY` (Claude API) → `OPENAI_API_KEY` (GPT) → the local **Claude Code CLI** in print mode (how the committed outputs were generated — Bedrock-hosted Claude) → clearly-labelled template fallbacks, so the pipeline always demonstrates end-to-end. Each prototype writes its generated emails, logs and registers to its own `sample_output/` folder (committed, so you can browse without running anything).

**Prompt logs:** every AI-using task folder contains a committed `prompt_log.md` — the actual system prompt, user message and Claude's real response on the sample data. Regenerate them all with `python3 shared/capture_prompt_logs.py`.

## Tools used and why

- **Claude** — primary: document classification, extraction, bilingual (EN/繁體中文) drafting, template filling.
- **GPT (ChatGPT)** — supported as an alternate provider in the same wrapper; used for comparison during prompt development.
- **Google Sheets + Apps Script** — master registers and the daily reminder trigger; free, auditable, and where the firm's staff already live.
- **Python (stdlib)** — demo harness so evaluators can run everything with zero setup.
- **WhatsApp Business API / WeCom** — production notification channels (mocked as drafts here; template-message approval is a noted dependency).

*All data is fabricated — no real client information anywhere in this repo.*
