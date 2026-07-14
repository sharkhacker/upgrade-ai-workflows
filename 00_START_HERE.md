# START HERE — Submission Overview

## AI Workflow Redesign — HK Company Secretarial Firm

**Submitted by:** Shrikant — AI & Automation Engineer (3–4 years building AI workflow automation for finance, GTM, HR and customer-support teams)

**What's in this submission**

- Written workflow designs for **all 12 tasks**, each with a flow diagram a non-technical reader can follow
- **6 working prototypes** (assessment asked for 3+), each run live on realistic dummy data
- Per task: **screenshots** of the automation running, the **actual Claude conversation** (prompt log), and the **generated outputs** — all committed in the task's folder

## A note on tooling

I use **Claude via the Claude Code CLI (AWS Bedrock-hosted)** rather than the claude.ai desktop app — it's how I run Claude day-to-day for automation work, and it means my prompt evidence is committed as exported conversation logs (`prompt_log.md` in each task folder, rendered as screenshots too) instead of claude.ai share links. Every log shows the real system prompt, the real input data, and Claude's actual response; all of it is regenerable with one command (`python3 shared/capture_prompt_logs.py`). The prototypes call the same CLI, so the committed outputs are genuine model output, not mock-ups.

## The 60-second version

Two ideas drive every design:

1. **Half of these tasks are one machine.** Deadline tracking, signing chasers, change-doc reminders and invoice dunning are all *register + clock + escalating reminder + human escalation*. I built that engine once (Google Sheets + Apps Script for production; Python for the demos) and configured it per task. The firm maintains one pattern, not six tools.

2. **AI drafts, humans decide, data stays out of the model.** Claude reads the letters, extracts the details, and writes personalized bilingual (EN/繁體中文) messages. But fees come from the fee schedule, deadlines from statutory date rules, and payment status only from a human. Every outbound message passes a named human checkpoint.

## What each prototype demonstrates

| Prototype | What the screenshots show |
|---|---|
| Task 1 — Correspondence triage | 6 letters (IRD notice, court writ, junk…) classified live; urgent items flagged `!!`; email + WhatsApp + WeChat 中文 drafts generated |
| Task 2 — Filing notifications | Deadline + scope + fee emails per client (in Chinese for Chinese-preference clients); NOA payment alerts scheduled T-14/7/1 |
| Task 3 — Master filing log | Deadlines *computed* from company records (NAR1 = anniversary + 42 days); daily digest with overdue items — deliberately no AI in the date math |
| Task 7 — Signing tracker | 7/14/21-day escalating chasers; internal escalation memo at stage 3 |
| Task 11 — Change-doc reminders | 已提供給客戶未簽回的變更文件 — every reminder in English *and* Traditional Chinese, tone escalating by stage |
| Task 12 — Invoicing & dunning | Invoice issue → courteous dunning sequence → human confirms payment → dunning stops, records update |

## How to review

The repo has **one folder per task** — folders named `prototype_task_NN_...` contain a working build, folders named `task_NN_...` are written designs. Each folder is self-contained:

- `README.md` / `DESIGN.md` — the write-up: flow diagram, trigger, AI steps, tools, human checkpoints, output, edge cases
- `prompt_log.md` + `screenshots/` — the real Claude conversation and images of the run and outputs
- `run.py` + `prompts/` + `sample_output/` — the automation itself (plain Python, no installs — run it yourself with `python3 run.py --today 2026-07-14`)

Design-only tasks (4, 5, 6, 9) include their own prompt logs and conversation screenshots; tasks 8 and 10 are powered by the task 3 and task 7 prototypes and link there.

*No real client data anywhere — all companies, letters and figures are fabricated.*
