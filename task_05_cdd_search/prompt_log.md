# Prompt Log — Task 5: CDD Search (screening-hit assessment)

*Captured 2026-07-14 via Claude Code CLI (print mode, Bedrock-hosted Claude). All data is fabricated sample data from [`data/`](../data/). Regenerate with `python3 shared/capture_prompt_logs.py`.*

### System prompt

```text
You summarise CDD screening results for a Hong Kong company secretarial firm. For each potential match below, assess match strength (name / DOB / nationality alignment), identify the list type, and give a plain-English rationale. Label everything 'for reviewer consideration' — the true/false match decision is made by the company secretary, never by you. End with a recommendation of which hits need escalation.
```

### User message

```text
Subject of search: CHEUNG Ka Ming Emily, DOB 1985-03-12, HK ID (partial) K8****(3), nationality: Chinese (Hong Kong). Director of Kowloon Bay F&B Group Limited.

Screening results (2 hits):
HIT 1: 'Emily CHEUNG' — adverse media, 2019 article on restaurant hygiene fines in Singapore. No DOB in source. Nationality: Singaporean.
HIT 2: 'CHEUNG Ka Ming' — PEP list, district council member, Hong Kong, DOB 1961-11-02, male.
```

### Claude's response

# CDD Screening Summary — For Reviewer Consideration

## Subject Profile
| Field | Detail |
|-------|--------|
| Name | CHEUNG Ka Ming Emily |
| Date of Birth | 12 March 1985 |
| HK ID (partial) | K8\*\*\*\*(3) |
| Nationality | Chinese (Hong Kong) |
| Role | Director, Kowloon Bay F&B Group Limited |

---

## Hit 1: "Emily CHEUNG" — Adverse Media

| Criterion | Assessment |
|-----------|------------|
| **List Type** | Adverse media (restaurant hygiene regulatory fines, Singapore, 2019) |
| **Name Alignment** | Partial — matches English given name + surname only; Chinese name "Ka Ming" absent from source |
| **DOB Alignment** | Unable to assess — no DOB recorded in the source article |
| **Nationality Alignment** | **Mismatch** — source individual is Singaporean; subject is Chinese (Hong Kong) |
| **Other Identifiers** | None available for comparison |

**Rationale:** The name overlap is limited to a common English name/surname combination. The stated nationality of the adverse-media subject (Singaporean) does not match our subject (Hong Kong Chinese). While both individuals are associated with the food & beverage sector — which is a surface-level contextual similarity — there is no corroborating identifier (DOB, ID number, address) to strengthen the link.

**Match Strength: LOW**

---

## Hit 2: "CHEUNG Ka Ming" — PEP List

| Criterion | Assessment |
|-----------|------------|
| **List Type** | Politically Exposed Person (PEP) — District Council member, Hong Kong |
| **Name Alignment** | Partial — matches Chinese name; English name "Emily" absent; PEP record implies male |
| **DOB Alignment** | **Clear mismatch** — PEP DOB is 2 November 1961 vs. subject's 12 March 1985 (24-year gap) |
| **Nationality Alignment** | Match — both Hong Kong |
| **Gender** | **Mismatch** — PEP record indicates male; subject's English name "Emily" indicates female |

**Rationale:** Although "CHEUNG Ka Ming" is a direct Chinese-name overlap and both are Hong Kong-based, the date of birth differs by 24 years and the gender indicators conflict (male district councillor vs. female director named "Emily"). "Cheung" is an extremely common Hong Kong surname, and "Ka Ming" is a widely-used given name across genders. The weight of the discrepancies (DOB + gender) substantially undermines this as a potential true match.

**Match Strength: LOW**

---

## Recommendation for Escalation

| Hit | Escalation Needed? | Reasoning |
|-----|-------------------|-----------|
| Hit 1 (Adverse Media) | **No — may be dismissed at first review** | Nationality mismatch with no corroborating identifiers. Insufficient basis to treat as a credible match. |
| Hit 2 (PEP) | **Borderline — flag for senior reviewer sign-off** | Although DOB and gender both conflict, the Chinese-name match is exact and both parties are Hong Kong-based. Given the regulatory expectation around PEP screening in Hong Kong (AMLO / HKMA guidance), conservative practice is to have a senior reviewer formally document the rationale for dismissal before closing. |

---

*This summary is prepared for reviewer consideration only. The determination of whether either hit constitutes a true match rests with the responsible Company Secretary / MLRO in accordance with the firm's CDD policies and applicable AML/CFT obligations.*

---
