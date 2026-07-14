# Prompt Log — Task 1: Incoming Correspondence Triage (court summons sample)

*Captured 2026-07-14 via Claude Code CLI (print mode, Bedrock-hosted Claude). All data is fabricated sample data from [`data/`](../data/). Regenerate with `python3 shared/capture_prompt_logs.py`.*

## Exchange 1

### System prompt

```text
You are the mailroom triage assistant for a Hong Kong company secretarial and
accounting firm. Clients use the firm's address as their registered office, so
all statutory mail arrives here first.

Classify each incoming item and respond with STRICT JSON only (no markdown, no
commentary) matching this schema:

{
  "category": "statutory_tax | statutory_cr | banking | legal_urgent | marketing_junk | physical_valuables | other",
  "client_name": "<company the item is addressed to, or null>",
  "sender": "<issuing organisation>",
  "summary": "<one sentence, plain English>",
  "deadline": "<YYYY-MM-DD if the letter contains an action deadline, else null>",
  "urgency": "urgent | normal | low",
  "notify_client": true/false,
  "notify_reason": "<why the client must (not) be told>",
  "suggested_action": "<next step for the firm>"
}

Rules:
- Court documents, writs, summons and anything with a statutory response
  window of 14 days or less => urgency "urgent" and notify_client true.
- Marketing material => notify_client false, urgency "low".
- Routine bank statements => notify_client false unless a discrepancy window
  is closing.
- Physical valuables (chops, share certificates, seals) => notify_client true
  and suggested_action must include secure storage confirmation.
```

### User message

```text
Classify this incoming item:

IN THE DISTRICT COURT OF THE
HONG KONG SPECIAL ADMINISTRATIVE REGION
CIVIL ACTION NO. 1234 OF 2026

Date: 11 July 2026

KOWLOON BAY F&B GROUP LIMITED
Shop 3-5, G/F, Telford Plaza
33 Wai Yip Street, Kowloon Bay

WRIT OF SUMMONS

TO THE DEFENDANT: You are hereby summoned to answer the claim of
Fresh Produce Wholesale Co. for the sum of HKD 187,400 in respect of
goods sold and delivered between January and April 2026.

IMPORTANT: If you do not acknowledge service within 14 DAYS of receipt,
judgment may be entered against you without further notice.

Registrar, District Court

```

### Claude's response

```json
{
  "category": "legal_urgent",
  "client_name": "Kowloon Bay F&B Group Limited",
  "sender": "District Court of Hong Kong",
  "summary": "Writ of Summons served by Fresh Produce Wholesale Co. claiming HKD 187,400 for unpaid goods delivered between January and April 2026.",
  "deadline": "2026-07-28",
  "urgency": "urgent",
  "notify_client": true,
  "notify_reason": "Court writ with a 14-day statutory window to acknowledge service; failure to respond risks default judgment against the client.",
  "suggested_action": "Immediately notify the client by phone and email, confirm receipt date for limitation purposes, scan and send a certified copy to the client's legal representative, and log the deadline (2026-07-28) in the firm's compliance tracker."
}
```

---

## Exchange 2

### System prompt

```text
You draft client notifications for a Hong Kong company secretarial firm.
Given a classified mail item and the client's contact record, produce three
versions of the same notification:

1. EMAIL — professional, subject line included, 80-150 words, signed
   "Client Services Team".
2. WHATSAPP — 2-4 short sentences, friendly but professional, no salutation
   heavier than "Hi <first name>".
3. WECHAT — same as WhatsApp but in Traditional Chinese (繁體中文) if the
   client's language preference is "zh", otherwise English.

Rules:
- State what was received, from whom, and the deadline (if any) in the first
  sentence.
- If urgency is "urgent", open with "URGENT:" in the email subject and lead
  with the deadline in all channels.
- Never give legal advice; for legal documents say we recommend they consult
  their legal adviser and that the original is available for collection.
- End every channel with a clear next step for the client.

Output format:

=== EMAIL ===
Subject: ...
<body>
=== WHATSAPP ===
<message>
=== WECHAT ===
<message>
```

### User message

```text
Client record: {"company_id": "C005", "name_en": "Kowloon Bay F&B Group Limited", "name_zh": "\u4e5d\u9f8d\u7063\u9910\u98f2\u96c6\u5718\u6709\u9650\u516c\u53f8", "brn": "71234565", "incorporation_date": "2017-05-09", "contact_name": "Emily Cheung", "email": "emily.cheung@kbfnb.example.hk", "phone": "+852 9123 0005", "preferred_channel": "whatsapp", "language": "zh", "services": "cosec,accounting,tax,payroll"}
Classified item: ```json
{
  "category": "legal_urgent",
  "client_name": "Kowloon Bay F&B Group Limited",
  "sender": "District Court of Hong Kong",
  "summary": "Writ of Summons for HKD 187,400 claim by Fresh Produce Wholesale Co. for goods sold and delivered, requiring acknowledgement of service within 14 days.",
  "deadline": "2026-07-28",
  "urgency": "urgent",
  "notify_client": true,
  "notify_reason": "Court writ with a 14-day statutory response window; failure to acknowledge service will result in default judgment against the client.",
  "suggested_action": "Immediately contact client by phone and email with scanned copy of the writ; confirm they have instructed solicitors to file acknowledgement of service before 28 July 2026; log deadline in the firm's compliance tracker."
}
```
```

### Claude's response

=== EMAIL ===
Subject: URGENT: Writ of Summons Received — Response Deadline 28 July 2026

Dear Emily,

We have received a Writ of Summons issued by the District Court of Hong Kong on behalf of Fresh Produce Wholesale Co., claiming HKD 187,400 for goods sold and delivered. An Acknowledgement of Service must be filed within 14 days — by **28 July 2026** — or a default judgment may be entered against Kowloon Bay F&B Group Limited.

Given the legal nature of this document, we strongly recommend that you instruct your solicitors immediately to handle the response within the statutory deadline. The original writ is available for collection at our office at your earliest convenience.

Please confirm receipt of this notice and let us know how you wish to proceed.

Client Services Team

=== WHATSAPP ===
Hi Emily, 🚨 deadline 28 July: we've received a Writ of Summons from the District Court of Hong Kong on behalf of Fresh Produce Wholesale Co. claiming HKD 187,400 against your company. We strongly recommend you instruct your solicitors immediately to file an Acknowledgement of Service before the deadline. The original document is ready for collection at our office — please let us know when you can arrange pickup or if you need a scanned copy sent over.

=== WECHAT ===
Emily 你好，🚨 限期 2026年7月28日：我們收到香港區域法院代 Fresh Produce Wholesale Co. 發出的傳訊令狀，向九龍灣餐飲集團有限公司追討港幣187,400元。請務必立即指示您的律師於限期前提交送達認收書，否則法庭可能會作出缺席判決。原件現可於本所領取，請告知何時方便安排取件或是否需要我們先發送掃描副本。

---
