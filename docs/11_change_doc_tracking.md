# Task 11 — Change-of-Document Tracking（已提供給客戶未簽回的變更文件）

> Email clients about documents provided but not yet signed back (Resignation/Appointment of Director or Company Secretary, Share Transfer, Change of Registered Office Address, Share Allotment); send reminder alerts to clients if unsigned, and reminders to the company secretary.

**Prototype: yes — [`prototypes/05_change_doc_reminders/`](../prototypes/05_change_doc_reminders/)**

## Why this design

Change documents are the highest-risk unsigned pile: each one has a statutory filing clock behind it (ND2A within 15 days of the change, NSC1 within a month of allotment…). And this firm's clients are bilingual — the demo data mirrors that with WeChat-preferred, Chinese-language contacts. So this workflow gets two upgrades over the generic chaser: **every reminder is drafted in English and Traditional Chinese**, and delivery follows the client's preferred channel.

## Workflow

| Step | Actor | Detail |
|---|---|---|
| Trigger | — | Change document issued to client (from document prep); register row created with type, sent date, expected signer, client language & channel |
| 1. Track | Automation | Daily scan; days outstanding computed per document |
| 2. Bilingual reminders | **Claude** | Stage 1 (7d, gentle) / stage 2 (14d, firm — states days outstanding and that the CR filing is blocked) / stage 3 (21d, final — statutory deadline language, 7-day respond-by, internal escalation). Both language versions in one call ([prompt](../shared/prompts/bilingual_change_doc_reminder.md)) |
| 3. Channel routing | Automation | Email / WhatsApp / WeChat per the client record — a Chinese-reading client gets 中文 on WeChat, not English in an inbox they don't check |
| 4. **Human checkpoint** | Staff approve reminders; secretary receives stage-3 escalations with full history |
| 5. Close | Automation | Signed document received → register updated → the underlying CR filing proceeds and the related deadline entry clears |

## Tools & why

- **Shared reminder engine** (third consumer, after tasks 7/10) — thresholds, register format and escalation logic identical; only the prompt and document taxonomy differ.
- **Claude for bilingual drafting** — genuinely equivalent 繁體中文, not machine-translated English; the demo template fallback includes proper Chinese business-letter register (台鑒 / 謹啟).

## Output

Live change-document register (`change_doc_register.csv` in the demo: stage-2 share transfer, two stage-3 escalations, one in grace, one returned), bilingual reminder drafts, and secretary escalation memos.

## Edge cases & escalations

- **Statutory clocks differ by document type** — ND2A's 15-day filing window means its thresholds tighten (5/10/15) in production config; the engine takes thresholds per document type.
- **Signer unavailable (travelling)** — client reply pauses the clock and records the reason; the secretary sees "paused: signer abroad until 8/1" instead of a silent gap.
- **Repeat offenders** — register history makes chronic non-returners visible for a relationship-level conversation, which no individual reminder can fix.
