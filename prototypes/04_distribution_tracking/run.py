"""Prototype 4 — Document distribution & signing tracker.

Covers tasks 7 (new company document packs) and 10 (annual return packs).
Scans the documents-out register, computes how long each item has been
awaiting signature, picks the escalation stage (7/14/21 days), and drafts
the appropriate chaser to the client — plus an internal escalation to the
company secretary at stage 3.

Run:  python3 run.py [--today 2026-07-14]
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "shared"))
import ai
import engine

CHASER_SYSTEM = """You draft signing-status chaser emails for a Hong Kong company
secretarial firm. Stage 1 = gentle nudge, stage 2 = firm (state days
outstanding, filings blocked), stage 3 = final (statutory deadline risk,
escalated internally, respond-by date 7 days out). Under 120 words,
sign 'Client Services Team'. Subject: "Reminder <stage>: <doc type> awaiting
your signature"."""


def template_chaser(client, doc, waiting, stage):
    tone = {1: "Just a friendly note that", 2: "This is our second reminder —",
            3: "FINAL REMINDER:"}[stage]
    return f"""Subject: Reminder {stage}: {doc['doc_type']} awaiting your signature

Dear {client['contact_name']},

[template mode] {tone} the "{doc['doc_type']}" we sent on {doc['sent_date']}
({waiting} days ago) is still awaiting your signature. We cannot proceed with
the related filing until the signed original is returned.
{"Statutory deadlines and late fees may be triggered; this matter has been escalated to our company secretary. Please respond within 7 days." if stage == 3 else "Please sign and return at your earliest convenience."}

Client Services Team
"""


def main():
    today = engine.today()
    print(f"AI provider: {ai.provider()} | run date: {today}\n")
    companies = engine.companies_by_id()
    escalations = []

    for doc in engine.load("documents_out.csv"):
        if doc["category"] == "change_doc":  # handled by prototype 5
            continue
        if doc["status"] != "awaiting_signature":
            print(f"OK   {doc['doc_id']} {doc['doc_type'][:48]:50s} signed & returned")
            continue
        waiting = -engine.days_until(doc["sent_date"], today)
        stage = engine.reminder_stage(waiting)
        client = companies[doc["company_id"]]
        if stage == 0:
            print(f"WAIT {doc['doc_id']} {doc['doc_type'][:48]:50s} {waiting}d — inside grace period")
            continue

        raw = ai.generate(
            f"Client: {json.dumps(client)}\nDocument: {json.dumps(doc)}\n"
            f"Days outstanding: {waiting}\nStage: {stage}\nToday: {today}",
            CHASER_SYSTEM,
        ) or template_chaser(client, doc, waiting, stage)
        out = engine.write_text(f"chasers/{doc['doc_id']}_stage{stage}.txt", raw)
        print(f"CHASE {doc['doc_id']} {doc['doc_type'][:48]:49s} {waiting}d -> stage {stage} "
              f"({engine.STAGE_LABEL[stage]}) -> {out.name}")

        if stage == 3:
            escalations.append(f"- {doc['doc_id']}: {doc['doc_type']} for {client['name_en']} "
                               f"unsigned {waiting} days (sent {doc['sent_date']})")

    if escalations:
        out = engine.write_text("secretary_escalation.txt",
            f"Subject: {len(escalations)} document(s) unsigned past 21 days — action needed\n"
            f"To: company.secretary@firm.example.hk\n\n" + "\n".join(escalations) +
            "\n\nSuggest phone follow-up; all client chasers to date attached.\n")
        print(f"\nInternal escalation -> {out.relative_to(engine.ROOT)}")
    print("Human checkpoint: chasers are drafts; secretary approves before sending.")


if __name__ == "__main__":
    main()
