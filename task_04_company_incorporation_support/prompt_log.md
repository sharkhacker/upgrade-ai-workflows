# Prompt Log — Task 4: Incorporation Support (checklist + information sheet)

*Captured 2026-07-14 via Claude Code CLI (print mode, Bedrock-hosted Claude). All data is fabricated sample data from [`data/`](../data/). Regenerate with `python3 shared/capture_prompt_logs.py`.*

### System prompt

```text
You are an incorporation support assistant for a Hong Kong company secretarial firm. Given the engagement details, produce: (1) a tailored document checklist for the client, (2) a short, friendly request email listing exactly what to send, and (3) the skeleton of the incorporation information sheet with every field we will need, marked TO COLLECT or PRE-FILLED from the engagement details.
```

### User message

```text
New engagement: proposed company 'Harbour Mist Coffee Limited' (中文名: 海霧咖啡有限公司). Two individual founders, both HK residents: Founder A will be sole director; both founders shareholders 60/40. 10,000 ordinary shares at HKD 1.00. Registered office: our firm's address. Company secretary: our firm. Nature of business: coffee shop chain.
```

### Claude's response

# Incorporation Support Package
## Harbour Mist Coffee Limited (海霧咖啡有限公司)

---

## 1. Document Checklist

| # | Document Required | From Whom | Notes |
|---|---|---|---|
| 1 | Clear copy of HKID card (front & back) | Founder A & Founder B | Must be valid and not expired |
| 2 | Proof of residential address (dated within 3 months) | Founder A & Founder B | Utility bill, bank statement, or govt correspondence |
| 3 | Signed Form NNC1 (Incorporation Form) | Founder A (as director) & both as subscribers | We will prepare for signature |
| 4 | Signed Articles of Association | Both founders | We will prepare standard form; advise if custom articles needed |
| 5 | Signed consent to act as director (Form NNC1 section) | Founder A | Included in NNC1 |
| 6 | Significant Controllers Register information | Both founders | Details of beneficial ownership |
| 7 | Business Registration application details | Founder A (as director) | Nature of business confirmation |
| 8 | KYC Declaration / Source of Funds | Founder A & Founder B | Standard AML/CFT compliance form |

---

## 2. Client Request Email

---

**Subject:** Documents Needed — Incorporation of Harbour Mist Coffee Limited

Hi [Founder A name] and [Founder B name],

Thank you for engaging us to incorporate **Harbour Mist Coffee Limited (海霧咖啡有限公司)**! We're excited to help you get started.

To proceed, could you please send us the following for **both founders**:

1. **Copy of your HKID card** — front and back, clear and legible
2. **Proof of residential address** — a recent utility bill, bank statement, or government letter dated within the last 3 months
3. **Completed KYC form** — attached to this email for your convenience

We will also need the following **personal details for each founder** (a simple reply to this email is fine):

- Full legal name in English and Chinese (as shown on HKID)
- HKID number
- Date of birth
- Residential address in full
- Nationality
- Contact email and mobile number
- Occupation

Once we have everything, we'll prepare the incorporation documents for your review and signature. The whole process typically takes **4–6 working days** from receipt of complete documents.

Please don't hesitate to reach out if you have any questions!

Best regards,
[Your Name]
[Firm Name]
Company Secretarial Team

---

## 3. Incorporation Information Sheet (Skeleton)

| Field | Status | Value / Notes |
|---|---|---|
| **COMPANY DETAILS** | | |
| Proposed English Name | ✅ PRE-FILLED | Harbour Mist Coffee Limited |
| Proposed Chinese Name | ✅ PRE-FILLED | 海霧咖啡有限公司 |
| Company Type | ✅ PRE-FILLED | Private company limited by shares |
| Nature of Business (English) | ✅ PRE-FILLED | Coffee shop chain |
| Business Registration Nature Code | 🔲 TO COLLECT | Confirm: "Restaurants and eating places" or similar |
| Registered Office Address | ✅ PRE-FILLED | [Firm's address] |
| Company Secretary | ✅ PRE-FILLED | [Firm name] |
| Financial Year End Date | 🔲 TO COLLECT | e.g. 31 March or 31 December |
| | | |
| **SHARE CAPITAL** | | |
| Class of Shares | ✅ PRE-FILLED | Ordinary |
| Total Shares to be Issued | ✅ PRE-FILLED | 10,000 |
| Par Value per Share | ✅ PRE-FILLED | HKD 1.00 |
| Total Share Capital | ✅ PRE-FILLED | HKD 10,000.00 |
| | | |
| **FOUNDER A (Director & Shareholder)** | | |
| Full Name (English) | 🔲 TO COLLECT | |
| Full Name (Chinese) | 🔲 TO COLLECT | |
| HKID Number | 🔲 TO COLLECT | |
| Date of Birth | 🔲 TO COLLECT | |
| Nationality | 🔲 TO COLLECT | |
| Residential Address | 🔲 TO COLLECT | |
| Correspondence Address | 🔲 TO COLLECT | (if different from residential) |
| Email | 🔲 TO COLLECT | |
| Mobile Number | 🔲 TO COLLECT | |
| Occupation | 🔲 TO COLLECT | |
| Role: Director | ✅ PRE-FILLED | Yes — sole director |
| Role: Shareholder | ✅ PRE-FILLED | Yes |
| No. of Shares Subscribed | ✅ PRE-FILLED | 6,000 (60%) |
| Amount Paid / Unpaid | 🔲 TO COLLECT | Confirm fully paid at incorporation? |
| Significant Controller? | ✅ PRE-FILLED | Yes (≥25% shares + sole director) |
| | | |
| **FOUNDER B (Shareholder only)** | | |
| Full Name (English) | 🔲 TO COLLECT | |
| Full Name (Chinese) | 🔲 TO COLLECT | |
| HKID Number | 🔲 TO COLLECT | |
| Date of Birth | 🔲 TO COLLECT | |
| Nationality | 🔲 TO COLLECT | |
| Residential Address | 🔲 TO COLLECT | |
| Correspondence Address | 🔲 TO COLLECT | (if different from residential) |
| Email | 🔲 TO COLLECT | |
| Mobile Number | 🔲 TO COLLECT | |
| Occupation | 🔲 TO COLLECT | |
| Role: Director | ✅ PRE-FILLED | No |
| Role: Shareholder | ✅ PRE-FILLED | Yes |
| No. of Shares Subscribed | ✅ PRE-FILLED | 4,000 (40%) |
| Amount Paid / Unpaid | 🔲 TO COLLECT | Confirm fully paid at incorporation? |
| Significant Controller? | ✅ PRE-FILLED | Yes (≥25% shares) |
| | | |
| **ARTICLES OF ASSOCIATION** | | |
| Type | 🔲 TO COLLECT | Standard Model Articles or customised? |
| Share Transfer Restrictions | 🔲 TO COLLECT | Pre-emption rights / board approval? |
| Quorum for Board Meetings | 🔲 TO COLLECT | Default = 1 (sole director) |
| Quorum for General Meetings | 🔲 TO COLLECT | Default = 2 members |
| | | |
| **ADDITIONAL MATTERS** | | |
| Bank Account Opening Needed? | 🔲 TO COLLECT | If yes, which bank preferred? |
| Business Registration Certificate (1 yr / 3 yr) | 🔲 TO COLLECT | 1-year (HKD 2,200) or 3-year (HKD 5,950)? |
| Chop / Company Seal Required? | 🔲 TO COLLECT | Round seal / rectangular chop / both? |
| Shareholders' Agreement in Place? | 🔲 TO COLLECT | Advisable given 60/40 split |

---

### Summary of Pre-filled vs. To Collect

| | Count |
|---|---|
| ✅ Pre-filled from engagement details | 16 fields |
| 🔲 Still to collect from clients | 28 fields |

**Next step:** Send the request email above and the KYC form to both founders. Once personal details and ID copies are received, we can prepare the NNC1 and Articles for signature and target filing within the week.

---
