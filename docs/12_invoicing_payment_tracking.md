# Task 12 — Invoicing & Payment Tracking

> Email invoices to clients, track payment status, and update internal records once payment is received.

**Prototype: yes — [`prototypes/06_invoicing_tracking/`](../prototypes/06_invoicing_tracking/)**

## Why this design

I've automated receivables follow-up for finance teams before, and the two rules that matter are: (1) the model never decides amounts or payment status — those are data; and (2) dunning tone must escalate *by policy*, not by model mood, because these are ongoing professional relationships. The automation decides *when and what stage*; the AI writes *the words*.

## Workflow

| Step | Actor | Detail |
|---|---|---|
| Trigger | — | Work completed (e.g. a filing marked done in the master log auto-creates a draft invoice from the fee schedule) — or monthly billing run |
| 1. Issue | **GPT/Claude** | Issue email drafted: thanks, service summary, amount, due date, payment methods ([prompt](../shared/prompts/dunning_sequence.md)); invoice PDF attached from the firm's template |
| 2. Track | Automation | Daily scan computes days overdue for every unpaid invoice |
| 3. Dunning | **GPT/Claude** | Stage 1 (1–14d, assume oversight) / stage 2 (15–30d, request a payment date, invite dispute) / stage 3 (30d+, final notice: work may pause, 7-day respond-by — still courteous) |
| 4. **Human checkpoint 1** | Accountant approves every outbound email |
| 5. Payment confirmation | **Human** | Only a human marks an invoice paid (`--mark-paid` in the prototype; bank-feed reconciliation *suggests* matches in production, a person confirms). Then: register updated, receipt email drafted, dunning halts instantly |
| 6. Escalation | Automation | Stage-3 items appear on a weekly aged-receivables summary for the partner, with relationship context (other active engagements, history) |

## Tools & why

- **Sheets register + Apps Script** — the firm-sized alternative to deploying an ERP; migrates cleanly to Xero/QuickBooks APIs later, with the AI layer unchanged.
- **AI only in the drafting seat** — amounts from the fee schedule, status from humans/bank data, stage from date math. The demo shows all five states: issue, dun-1, dun-2, paid, current.

## Output

Issue and dunning drafts (`outputs/invoicing/`), a live action log, and a register where "who owes us what and how long" is a filter, not an afternoon of reconciliation.

## Edge cases & escalations

- **Disputed invoices** — a reply pauses dunning and routes to the accountant; you must never dun a client who's asked a question.
- **Payment received between scan and send** — approval queue re-checks status at send time.
- **Chronic late payers** — history feeds the partner summary; the fix is commercial terms (deposits), not a fourth reminder.
- **Work-pause warnings (stage 3)** — flagged to the engagement owner *before* sending, since pausing statutory work has compliance consequences for the client.
