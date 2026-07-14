# Prompt Log — Task 6: Document Preparation (first minutes — note the MISSING refusals)

*Captured 2026-07-14 via Claude Code CLI (print mode, Bedrock-hosted Claude). All data is fabricated sample data from [`data/`](../data/). Regenerate with `python3 shared/capture_prompt_logs.py`.*

### System prompt

```text
You prepare corporate documents for a Hong Kong company secretarial firm. Fill the FIRST BOARD MINUTES template using only facts from the company record JSON below. Rules: use template wording exactly; replace only {{placeholders}}. Names must match the record character-for-character (including 中文 names). If a required fact is missing from the record, output 'MISSING: <field>' instead of guessing.
```

### User message

```text
Company record: {"company_id": "C004", "name_en": "Lion Rock Technologies Limited", "name_zh": "獅子山科技有限公司", "brn": "71234564", "incorporation_date": "2022-07-28", "contact_name": "David Ng", "email": "david.ng@lionrocktech.example.hk", "phone": "+852 9123 0004", "preferred_channel": "email", "language": "en", "services": "cosec,accounting"}

Template:
MINUTES of the first meeting of the board of directors of {{name_en}} ({{name_zh}}) held at {{registered_office_address}} on {{meeting_date}}.
PRESENT: {{directors_present}}
1. INCORPORATION: noted certificate of incorporation no. {{brn}} dated {{incorporation_date}}.
2. FIRST DIRECTOR(S): {{directors_present}} appointed per NNC1.
3. REGISTERED OFFICE: resolved the registered office be at {{registered_office_address}}.
4. SHARE ISSUE: resolved that {{share_allotment_details}} be allotted.
Signed: {{chairperson}}
```

### Claude's response

MINUTES of the first meeting of the board of directors of Lion Rock Technologies Limited (獅子山科技有限公司) held at MISSING: <registered_office_address> on MISSING: <meeting_date>.

PRESENT: MISSING: <directors_present>

1. INCORPORATION: noted certificate of incorporation no. 71234564 dated 2022-07-28.
2. FIRST DIRECTOR(S): MISSING: <directors_present> appointed per NNC1.
3. REGISTERED OFFICE: resolved the registered office be at MISSING: <registered_office_address>.
4. SHARE ISSUE: resolved that MISSING: <share_allotment_details> be allotted.

Signed: MISSING: <chairperson>

---

**Summary of fields filled from the company record:**
| Placeholder | Value |
|---|---|
| `{{name_en}}` | Lion Rock Technologies Limited |
| `{{name_zh}}` | 獅子山科技有限公司 |
| `{{brn}}` | 71234564 |
| `{{incorporation_date}}` | 2022-07-28 |

**Fields marked MISSING (not present in the record):**
| Placeholder | Reason |
|---|---|
| `{{registered_office_address}}` | No address in record |
| `{{meeting_date}}` | No meeting date in record |
| `{{directors_present}}` | No director names in record (contact_name "David Ng" is not identified as a director) |
| `{{share_allotment_details}}` | No share information in record |
| `{{chairperson}}` | No chairperson identified in record |

Please provide the missing details and I can produce the completed minutes.

---
