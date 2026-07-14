# START HERE — Submission Overview

*(Copy this into a Google Doc at the top of the shared Drive folder — it's the front door for reviewers. Replace the bracketed links after uploading.)*

---

## AI Workflow Redesign — HK Company Secretarial Firm

**Submitted by:** Shrikant — AI & Automation Engineer (3–4 years building AI workflow automation for finance, GTM, HR and customer-support teams)

**What's in this submission**

- Written workflow designs for **all 12 tasks**
- **6 working prototypes** (assessment asked for 3+), each demonstrated on realistic dummy data
- Screen recordings of each prototype running: **[Drive: /recordings]**
- Full source, prompts and sample data: **[GitHub repo link]** (public)

## The 60-second version

Two ideas drive every design:

1. **Half of these tasks are one machine.** Deadline tracking, signing chasers, change-doc reminders and invoice dunning are all *register + clock + escalating reminder + human escalation*. I built that engine once (Google Sheets + Apps Script for production; Python for the demos) and configured it per task. The firm maintains one pattern, not six tools.

2. **AI drafts, humans decide, data stays out of the model.** Claude/GPT read the letters, extract the details, and write personalized bilingual (EN/繁體中文) messages. But fees come from the fee schedule, deadlines from statutory date rules, and payment status only from a human. Every outbound message passes a named human checkpoint.

## What each prototype shows (with recordings)

| Prototype | Watch | What you'll see |
|---|---|---|
| P1 Correspondence triage | [link] | 6 letters (IRD notice, court writ, junk…) classified, logged, urgent flagged, email/WhatsApp/WeChat drafts generated |
| P2 Filing notifications | [link] | Deadline + scope + fee emails per client; NOA payment alerts scheduled T-14/7/1 |
| P3 Master filing log | [link] | Deadlines *computed* from company records (NAR1 = anniversary+42d); daily digest with overdue items |
| P4 Signing tracker | [link] | 7/14/21-day escalating chasers; internal escalation memo at stage 3 |
| P5 Bilingual change-doc reminders | [link] | 已提供給客戶未簽回的變更文件 — every reminder in English *and* Traditional Chinese, tone escalating by stage |
| P6 Invoicing & dunning | [link] | Invoice issue → polite dunning sequence → human confirms payment → records update |

## Where to go next

The repo has **one folder per task** — folders named `prototype_task_NN_...` contain a working build, folders named `task_NN_...` are written designs. Each folder is self-contained: the design write-up (trigger, AI steps, tools, human checkpoints, output, edge cases), plus for prototypes the runnable code, its AI prompts, and committed sample outputs so you can review results without running anything.

- **Non-technical readers:** open any task folder and read the README/DESIGN — each is 1–2 pages of plain language.
- **Technical readers:** every prototype runs with plain Python, no installs — instructions in each folder's README.

*No real client data anywhere — all companies, letters and figures are fabricated.*
