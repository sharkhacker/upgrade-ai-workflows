# Prompt Log — Task 2: Statutory Filing Notification (Employer's Return 56AB)

*Captured 2026-07-14 via Claude Code CLI (print mode, Bedrock-hosted Claude). All data is fabricated sample data from [`data/`](../data/). Regenerate with `python3 shared/capture_prompt_logs.py`.*

### System prompt

```text
You draft statutory filing notification emails for a Hong Kong CPA /
company secretarial firm. Each email must contain, in this order:

1. The filing obligation and its exact statutory deadline.
2. The consequence of missing it (penalty/higher fee, one sentence, factual
   not scary).
3. What our firm will do — restate the service description in client-friendly
   language.
4. The proposed fee in HKD, presented as a simple one-line quotation.
5. A clear call to action: reply to confirm engagement by a stated date
   (deadline minus 14 days), or contact us with questions.

Tone: professional, warm, concise (under 200 words). Sign off as
"Client Services Team". Subject line format:
"[Action required] <Filing type> — due <date> — <Company name>"
```

### User message

```text
Company: {"company_id": "C005", "name_en": "Kowloon Bay F&B Group Limited", "name_zh": "\u4e5d\u9f8d\u7063\u9910\u98f2\u96c6\u5718\u6709\u9650\u516c\u53f8", "brn": "71234565", "incorporation_date": "2017-05-09", "contact_name": "Emily Cheung", "email": "emily.cheung@kbfnb.example.hk", "phone": "+852 9123 0005", "preferred_channel": "whatsapp", "language": "zh", "services": "cosec,accounting,tax,payroll"}
Filing: {"filing_id": "F005", "company_id": "C005", "filing_type": "56AB", "description": "Employer's Return 2025/26", "due_date": "2026-07-31", "status": "pending"}
Service & fee: {"filing_type": "56AB", "service_description": "Preparation and filing of Employer's Return (BIR56A + IR56B forms) for all employees, including payroll data reconciliation", "fee_hkd": "1800"}
Today's date: 2026-07-14
```

### Claude's response

**Subject:** [需要回覆] 僱主報稅表 (56AB) — 截止日期 2026年7月31日 — 九龍灣餐飲集團有限公司

---

Emily 您好，

謹此通知以下法定申報事項：

**1. 申報責任及截止日期**
貴公司須根據《稅務條例》提交 2025/26 年度僱主報稅表（BIR56A 連同 IR56B 表格），法定截止日期為 **2026年7月31日**。

**2. 逾期後果**
逾期提交可能導致稅務局發出罰款通知或提起檢控。

**3. 我們的服務**
本所將為貴公司核對薪酬數據，編製及提交僱主報稅表（BIR56A）及所有僱員的 IR56B 表格，確保準確合規。

**4. 收費**
服務費用：**HKD 1,800**

**5. 下一步**
請於 **2026年7月17日** 或之前回覆本郵件確認委託，以便我們有充足時間處理。如有任何疑問，歡迎隨時與我們聯絡。

順祝 商祺

Client Services Team

---
