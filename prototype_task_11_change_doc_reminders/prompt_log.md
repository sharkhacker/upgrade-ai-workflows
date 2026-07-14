# Prompt Log — Task 11: Bilingual Change-Document Reminder (stage 3, EN + 繁體中文)

*Captured 2026-07-14 via Claude Code CLI (print mode, Bedrock-hosted Claude). All data is fabricated sample data from [`data/`](../data/). Regenerate with `python3 shared/capture_prompt_logs.py`.*

### System prompt

```text
You draft signing reminders for a Hong Kong company secretarial firm, in
BOTH English and Traditional Chinese (繁體中文), for corporate change
documents sent to clients but not yet signed and returned. Document types:
Resignation/Appointment of Director or Company Secretary (ND2A), Share
Transfer, Change of Registered Office Address (NR1), Share Allotment (NSC1).

You will be told the reminder STAGE:
- Stage 1 (gentle): assume they've been busy; short friendly nudge.
- Stage 2 (firm): note this is the second reminder, state how many days the
  document has been outstanding, and mention the filing cannot proceed
  without it.
- Stage 3 (final): state that statutory deadlines and late fees may be
  triggered, that the matter is being escalated to our company secretary,
  and give a specific respond-by date (7 days from today).

Output format:

=== ENGLISH ===
Subject: ...
<body, max 120 words>
=== 中文 ===
主旨：...
<body in Traditional Chinese, equivalent content>
```

### User message

```text
Client: {"company_id": "C005", "name_en": "Kowloon Bay F&B Group Limited", "name_zh": "九龍灣餐飲集團有限公司", "brn": "71234565", "incorporation_date": "2017-05-09", "contact_name": "Emily Cheung", "email": "emily.cheung@kbfnb.example.hk", "phone": "+852 9123 0005", "preferred_channel": "whatsapp", "language": "zh", "services": "cosec,accounting,tax,payroll"}
Document: {"doc_id": "D005", "company_id": "C005", "doc_type": "Resignation and Appointment of Director (ND2A)", "category": "change_doc", "sent_date": "2026-06-15", "status": "awaiting_signature", "signer": "Emily Cheung"}
Days outstanding: 29
Reminder stage: 3
Today's date: 2026-07-14
```

### Claude's response

=== ENGLISH ===
Subject: FINAL REMINDER – ND2A (Director Change) Awaiting Your Signature [Kowloon Bay F&B Group Limited]

Dear Emily,

This is our third and final reminder regarding the Resignation and Appointment of Director form (ND2A) for Kowloon Bay F&B Group Limited (BRN: 71234565), sent to you on 15 June 2026 — now outstanding for 29 days.

Under the Companies Ordinance (Cap. 622), the ND2A must be filed within 15 days of the effective date of the directorship change. The statutory deadline has likely already passed, and continued delay will trigger late filing fees imposed by the Companies Registry.

This matter is now being escalated to our Company Secretary for further action.

**Please sign and return the document by 21 July 2026 at the latest.** If we do not receive the signed form by this date, we may be unable to prevent penalties from accruing on behalf of your company.

Should you have any questions or require assistance, please contact us immediately.

Regards,
Corporate Secretarial Team

=== 中文 ===
主旨：【最後提醒】九龍灣餐飲集團有限公司 — 董事變更表格（ND2A）尚待簽署

Emily 您好，

此為第三次亦是最後一次提醒，有關 九龍灣餐飲集團有限公司（商業登記號碼：71234565）之董事辭任及委任表格（ND2A），該文件已於2026年6月15日發出，至今已逾 29天 仍未獲簽回。

根據《公司條例》（第622章），ND2A須於董事變更生效日期起計15天內提交公司註冊處。法定期限很可能已届滿，持續延誤將導致公司註冊處徵收逾期申報費用。

本事項現已升級交由本所公司秘書跟進處理。

**請務必於2026年7月21日或之前簽署並交回文件。** 若届時仍未收到已簽署表格，本所將無法為 貴公司避免相關罰款。

如有任何疑問或需要協助，請即與我們聯絡。

此致
公司秘書部

---
