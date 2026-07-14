"""Capture real prompt logs for every task.

Runs each task's actual prompts (with sample data from data/) through the
configured AI provider — on this machine, Claude Code CLI in print mode,
Bedrock-hosted — and writes the full conversation to prompt_log.md in the
task's folder. Re-runnable: delete a log and run again to regenerate.

    python3 shared/capture_prompt_logs.py [task_number ...]
"""
import datetime
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import ai
import engine

ROOT = engine.ROOT
TODAY = "2026-07-14"


def _prompt_block(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8").split("```")[1].strip()


def _row(name: str, **match) -> dict:
    for row in engine.load(name):
        if all(row[k] == v for k, v in match.items()):
            return row
    raise KeyError(match)


def write_log(folder: str, title: str, exchanges: list[tuple[str, str]]):
    """exchanges: list of (system, user) pairs; responses come from the model."""
    lines = [
        f"# Prompt Log — {title}",
        "",
        f"*Captured {datetime.date.today()} via Claude Code CLI (print mode, "
        "Bedrock-hosted Claude). All data is fabricated sample data from "
        "[`data/`](../data/). Regenerate with "
        "`python3 shared/capture_prompt_logs.py`.*",
        "",
    ]
    for i, (system, user) in enumerate(exchanges, 1):
        print(f"  [{i}/{len(exchanges)}] calling model...", flush=True)
        response = ai.generate(user, system) or "(no AI provider available)"
        if len(exchanges) > 1:
            lines += [f"## Exchange {i}", ""]
        lines += [
            "### System prompt", "", "```text", system, "```", "",
            "### User message", "", "```text", user, "```", "",
            "### Claude's response", "", response, "", "---", "",
        ]
    out = ROOT / folder / "prompt_log.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"  -> {out.relative_to(ROOT)}")


def task_01():
    classifier = _prompt_block(ROOT / "prototype_task_01_correspondence_triage/prompts/correspondence_classifier.md")
    notifier = _prompt_block(ROOT / "prototype_task_01_correspondence_triage/prompts/client_notification.md")
    letter = (engine.DATA / "correspondence/letter_05_court_summons.txt").read_text(encoding="utf-8")
    client = _row("companies.csv", company_id="C005")
    # first classify, then draft notifications from the real classifier output
    classification = ai.generate(f"Classify this incoming item:\n\n{letter}", classifier) or "{}"
    write_log(
        "prototype_task_01_correspondence_triage",
        "Task 1: Incoming Correspondence Triage (court summons sample)",
        [
            (classifier, f"Classify this incoming item:\n\n{letter}"),
            (notifier, f"Client record: {json.dumps(client)}\nClassified item: {classification}"),
        ],
    )


def task_02():
    system = _prompt_block(ROOT / "prototype_task_02_filing_notifications/prompts/filing_notification.md")
    company = _row("companies.csv", company_id="C005")
    filing = _row("filings.csv", filing_id="F005")
    fee = _row("fee_schedule.csv", filing_type="56AB")
    write_log(
        "prototype_task_02_filing_notifications",
        "Task 2: Statutory Filing Notification (Employer's Return 56AB)",
        [(system, f"Company: {json.dumps(company)}\nFiling: {json.dumps(filing)}\n"
                  f"Service & fee: {json.dumps(fee)}\nToday's date: {TODAY}")],
    )


def task_04():
    system = (
        "You are an incorporation support assistant for a Hong Kong company "
        "secretarial firm. Given the engagement details, produce: (1) a tailored "
        "document checklist for the client, (2) a short, friendly request email "
        "listing exactly what to send, and (3) the skeleton of the incorporation "
        "information sheet with every field we will need, marked TO COLLECT or "
        "PRE-FILLED from the engagement details."
    )
    user = (
        "New engagement: proposed company 'Harbour Mist Coffee Limited' "
        "(中文名: 海霧咖啡有限公司). Two individual founders, both HK residents: "
        "Founder A will be sole director; both founders shareholders 60/40. "
        "10,000 ordinary shares at HKD 1.00. Registered office: our firm's address. "
        "Company secretary: our firm. Nature of business: coffee shop chain."
    )
    write_log("task_04_company_incorporation_support",
              "Task 4: Incorporation Support (checklist + information sheet)",
              [(system, user)])


def task_05():
    system = (
        "You summarise CDD screening results for a Hong Kong company secretarial "
        "firm. For each potential match below, assess match strength (name / DOB / "
        "nationality alignment), identify the list type, and give a plain-English "
        "rationale. Label everything 'for reviewer consideration' — the true/false "
        "match decision is made by the company secretary, never by you. "
        "End with a recommendation of which hits need escalation."
    )
    user = (
        "Subject of search: CHEUNG Ka Ming Emily, DOB 1985-03-12, HK ID (partial) "
        "K8****(3), nationality: Chinese (Hong Kong). Director of Kowloon Bay F&B "
        "Group Limited.\n\nScreening results (2 hits):\n"
        "HIT 1: 'Emily CHEUNG' — adverse media, 2019 article on restaurant hygiene "
        "fines in Singapore. No DOB in source. Nationality: Singaporean.\n"
        "HIT 2: 'CHEUNG Ka Ming' — PEP list, district council member, Hong Kong, "
        "DOB 1961-11-02, male."
    )
    write_log("task_05_cdd_search",
              "Task 5: CDD Search (screening-hit assessment)",
              [(system, user)])


def task_06():
    system = (
        "You prepare corporate documents for a Hong Kong company secretarial firm. "
        "Fill the FIRST BOARD MINUTES template using only facts from the company "
        "record JSON below. Rules: use template wording exactly; replace only "
        "{{placeholders}}. Names must match the record character-for-character "
        "(including 中文 names). If a required fact is missing from the record, "
        "output 'MISSING: <field>' instead of guessing."
    )
    company = _row("companies.csv", company_id="C004")
    template = (
        "MINUTES of the first meeting of the board of directors of "
        "{{name_en}} ({{name_zh}}) held at {{registered_office_address}} on "
        "{{meeting_date}}.\nPRESENT: {{directors_present}}\n"
        "1. INCORPORATION: noted certificate of incorporation no. {{brn}} dated "
        "{{incorporation_date}}.\n2. FIRST DIRECTOR(S): {{directors_present}} "
        "appointed per NNC1.\n3. REGISTERED OFFICE: resolved the registered office "
        "be at {{registered_office_address}}.\n4. SHARE ISSUE: resolved that "
        "{{share_allotment_details}} be allotted.\nSigned: {{chairperson}}"
    )
    # company record has no registered office, meeting date or share details ->
    # the model must refuse with MISSING rather than invent them
    write_log("task_06_incorporation_document_prep",
              "Task 6: Document Preparation (first minutes — note the MISSING refusals)",
              [(system, f"Company record: {json.dumps(company, ensure_ascii=False)}\n\nTemplate:\n{template}")])


def task_07():
    system = (
        "You draft signing-status chaser emails for a Hong Kong company secretarial "
        "firm. Stage 1 = gentle nudge, stage 2 = firm (state days outstanding, "
        "filings blocked), stage 3 = final (statutory deadline risk, escalated "
        "internally, respond-by date 7 days out). Under 120 words, sign 'Client "
        "Services Team'. Subject: \"Reminder <stage>: <doc type> awaiting your signature\"."
    )
    client = _row("companies.csv", company_id="C001")
    doc = _row("documents_out.csv", doc_id="D002")
    base = (f"Client: {json.dumps(client)}\nDocument: {json.dumps(doc)}\n"
            f"Today: {TODAY}\n")
    write_log(
        "prototype_task_07_doc_distribution_tracking",
        "Task 7: Signing Chasers (stage 1 vs stage 3 — same document, escalating tone)",
        [
            (system, base + "Days outstanding: 13\nStage: 1"),
            (system, base + "Days outstanding: 25\nStage: 3"),
        ],
    )


def task_09():
    system = (
        "You prepare Hong Kong Annual Return (NAR1) data for a company secretarial "
        "firm. Using the company record JSON (current state) and last year's NAR1 "
        "data JSON, produce: 1. NAR1_DATA — the complete field set for a return "
        "made up to the return date, using current-state facts; never carry forward "
        "a fact the current record contradicts; if a required field is missing, "
        "output 'MISSING: <field>'. 2. CHANGE_SUMMARY — a plain-English paragraph "
        "listing every difference from last year's return, citing the filing that "
        "effected each change where available. If nothing changed, say exactly that."
    )
    current = {
        "name_en": "Golden Harbour Trading Limited", "name_zh": "金港貿易有限公司",
        "brn": "71234561", "return_date": "2026-08-02",
        "registered_office": "Suite 2101, Harbour Centre, 25 Harbour Road, Wan Chai",
        "directors": ["CHAN Wai Ling Alice"], "company_secretary": "Our Firm CS Limited",
        "share_capital": {"class": "ordinary", "total_shares": 10000,
                          "members": [{"name": "CHAN Wai Ling Alice", "shares": 10000}]},
        "changes_filed_this_year": [
            {"form": "ND2A", "date": "2026-03-02",
             "detail": "WONG Siu Keung resigned as director"},
            {"form": "instrument of transfer", "date": "2026-03-15",
             "detail": "WONG Siu Keung transferred 4,000 shares to CHAN Wai Ling Alice"},
        ],
    }
    last_year = {
        "return_date": "2025-08-02",
        "registered_office": "Suite 2101, Harbour Centre, 25 Harbour Road, Wan Chai",
        "directors": ["CHAN Wai Ling Alice", "WONG Siu Keung"],
        "company_secretary": "Our Firm CS Limited",
        "share_capital": {"class": "ordinary", "total_shares": 10000,
                          "members": [{"name": "CHAN Wai Ling Alice", "shares": 6000},
                                      {"name": "WONG Siu Keung", "shares": 4000}]},
    }
    write_log("task_09_annual_return_preparation",
              "Task 9: Annual Return Roll-Forward (with change summary)",
              [(system, f"Current record: {json.dumps(current, ensure_ascii=False)}\n\n"
                        f"Last year's NAR1: {json.dumps(last_year, ensure_ascii=False)}")])


def task_11():
    system = _prompt_block(ROOT / "prototype_task_11_change_doc_reminders/prompts/bilingual_change_doc_reminder.md")
    client = _row("companies.csv", company_id="C005")
    doc = _row("documents_out.csv", doc_id="D005")
    write_log(
        "prototype_task_11_change_doc_reminders",
        "Task 11: Bilingual Change-Document Reminder (stage 3, EN + 繁體中文)",
        [(system, f"Client: {json.dumps(client, ensure_ascii=False)}\n"
                  f"Document: {json.dumps(doc, ensure_ascii=False)}\n"
                  f"Days outstanding: 29\nReminder stage: 3\nToday's date: {TODAY}")],
    )


def task_12():
    system = _prompt_block(ROOT / "prototype_task_12_invoicing_payment_tracking/prompts/dunning_sequence.md")
    client = _row("companies.csv", company_id="C005")
    inv = _row("invoices.csv", invoice_no="INV-2026-035")
    write_log(
        "prototype_task_12_invoicing_payment_tracking",
        "Task 12: Invoice Dunning (stage 2 — firm but courteous)",
        [(system, f"Client: {json.dumps(client)}\nInvoice: {json.dumps(inv)}\n"
                  f"Mode: dunning stage 2\nDays overdue: 17\nToday's date: {TODAY}")],
    )


ALL = {"01": task_01, "02": task_02, "04": task_04, "05": task_05,
       "06": task_06, "07": task_07, "09": task_09, "11": task_11, "12": task_12}

if __name__ == "__main__":
    picked = [a.zfill(2) for a in sys.argv[1:]] or list(ALL)
    print(f"AI provider: {ai.provider()}")
    for key in picked:
        print(f"Task {key}:")
        ALL[key]()
    print("DONE")
