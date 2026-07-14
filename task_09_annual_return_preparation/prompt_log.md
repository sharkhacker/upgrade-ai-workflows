# Prompt Log — Task 9: Annual Return Roll-Forward (with change summary)

*Captured 2026-07-14 via Claude Code CLI (print mode, Bedrock-hosted Claude). All data is fabricated sample data from [`data/`](../data/). Regenerate with `python3 shared/capture_prompt_logs.py`.*

### System prompt

```text
You prepare Hong Kong Annual Return (NAR1) data for a company secretarial firm. Using the company record JSON (current state) and last year's NAR1 data JSON, produce: 1. NAR1_DATA — the complete field set for a return made up to the return date, using current-state facts; never carry forward a fact the current record contradicts; if a required field is missing, output 'MISSING: <field>'. 2. CHANGE_SUMMARY — a plain-English paragraph listing every difference from last year's return, citing the filing that effected each change where available. If nothing changed, say exactly that.
```

### User message

```text
Current record: {"name_en": "Golden Harbour Trading Limited", "name_zh": "金港貿易有限公司", "brn": "71234561", "return_date": "2026-08-02", "registered_office": "Suite 2101, Harbour Centre, 25 Harbour Road, Wan Chai", "directors": ["CHAN Wai Ling Alice"], "company_secretary": "Our Firm CS Limited", "share_capital": {"class": "ordinary", "total_shares": 10000, "members": [{"name": "CHAN Wai Ling Alice", "shares": 10000}]}, "changes_filed_this_year": [{"form": "ND2A", "date": "2026-03-02", "detail": "WONG Siu Keung resigned as director"}, {"form": "instrument of transfer", "date": "2026-03-15", "detail": "WONG Siu Keung transferred 4,000 shares to CHAN Wai Ling Alice"}]}

Last year's NAR1: {"return_date": "2025-08-02", "registered_office": "Suite 2101, Harbour Centre, 25 Harbour Road, Wan Chai", "directors": ["CHAN Wai Ling Alice", "WONG Siu Keung"], "company_secretary": "Our Firm CS Limited", "share_capital": {"class": "ordinary", "total_shares": 10000, "members": [{"name": "CHAN Wai Ling Alice", "shares": 6000}, {"name": "WONG Siu Keung", "shares": 4000}]}}
```

### Claude's response

## NAR1_DATA

**Annual Return made up to: 2 August 2026**

| Field | Value |
|-------|-------|
| **Company Name (English)** | Golden Harbour Trading Limited |
| **Company Name (Chinese)** | 金港貿易有限公司 |
| **Business Registration No.** | 71234561 |
| **Date of This Return** | 2026-08-02 |
| **Registered Office** | Suite 2101, Harbour Centre, 25 Harbour Road, Wan Chai |
| **Director(s)** | CHAN Wai Ling Alice |
| **Company Secretary** | Our Firm CS Limited |
| **Share Capital — Class** | Ordinary |
| **Share Capital — Total Shares** | 10,000 |
| **Member 1** | CHAN Wai Ling Alice — 10,000 shares |

> **MISSING fields (not in source record):** Director's residential address; Director's ID/passport number and issuing country; Director's date of appointment; Company number (CI number); Date of last AGM; Particulars of company secretary (address, ID/licence number).

---

## CHANGE_SUMMARY

Compared with the Annual Return made up to 2 August 2025, two changes have occurred. First, WONG Siu Keung ceased to be a director, effected by Form ND2A filed on 2 March 2026. Second, WONG Siu Keung's 4,000 ordinary shares were transferred to CHAN Wai Ling Alice (per instrument of transfer dated 15 March 2026), making CHAN Wai Ling Alice the sole member holding all 10,000 shares; WONG Siu Keung is accordingly removed from the register of members. All other particulars — registered office, company secretary, total issued share capital, and share class — remain unchanged.

---
