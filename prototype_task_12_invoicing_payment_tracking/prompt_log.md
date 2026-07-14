# Prompt Log — Task 12: Invoice Dunning (stage 2 — firm but courteous)

*Captured 2026-07-14 via Claude Code CLI (print mode, Bedrock-hosted Claude). All data is fabricated sample data from [`data/`](../data/). Regenerate with `python3 shared/capture_prompt_logs.py`.*

### System prompt

```text
You draft invoicing emails for a Hong Kong CPA / company secretarial firm.

MODES:
- "issue": first delivery of the invoice. Thank the client for their
  business, summarise the service, state amount (HKD) and due date, and give
  payment methods (FPS ID 123456789, or cheque payable to the firm).
- "dunning stage 1" (1-14 days overdue): polite nudge; assume oversight;
  re-attach invoice reference.
- "dunning stage 2" (15-30 days overdue): firm; state days overdue; request
  payment date; offer to discuss if there is an issue with the invoice.
- "dunning stage 3" (30+ days overdue): final notice; state that ongoing
  statutory work may be paused and the account escalated; give a 7-day
  respond-by date. Still courteous — this is a professional services
  relationship, not debt collection.

Always under 150 words. Subject format:
"Invoice <no> — <company> — <'due ' + date | n + ' days overdue'>"
Sign off "Accounts Team".
```

### User message

```text
Client: {"company_id": "C005", "name_en": "Kowloon Bay F&B Group Limited", "name_zh": "\u4e5d\u9f8d\u7063\u9910\u98f2\u96c6\u5718\u6709\u9650\u516c\u53f8", "brn": "71234565", "incorporation_date": "2017-05-09", "contact_name": "Emily Cheung", "email": "emily.cheung@kbfnb.example.hk", "phone": "+852 9123 0005", "preferred_channel": "whatsapp", "language": "zh", "services": "cosec,accounting,tax,payroll"}
Invoice: {"invoice_no": "INV-2026-035", "company_id": "C005", "description": "Employer's Return 56AB + payroll service Q2", "amount_hkd": "3300", "issue_date": "2026-05-28", "due_date": "2026-06-27", "status": "overdue", "paid_date": ""}
Mode: dunning stage 2
Days overdue: 17
Today's date: 2026-07-14
```

### Claude's response

**Subject:** Invoice INV-2026-035 — Kowloon Bay F&B Group Limited — 17 days overdue

---

Emily 你好，

關於發票 INV-2026-035（僱主報稅表 56AB + 第二季薪俸服務），金額為 HKD 3,300，到期日為 2026年6月27日，現已逾期 **17天**，至今仍未收到款項。

煩請告知預計付款日期。如對此發票有任何疑問或需要商討安排，歡迎隨時聯絡我們。

付款方式：
- 轉數快 FPS ID：123456789
- 支票抬頭：本行名稱

期待您的回覆。

Accounts Team

---
