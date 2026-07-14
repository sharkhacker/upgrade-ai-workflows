"""Prototype 2 — Statutory filing notifications + payment alerts.

For every pending filing due within the notification window, generates the
client email containing deadline + scope of CPA work + proposed fee.
For Notices of Assessment (tax payment), builds a time-based payment alert
schedule (T-14 / T-7 / T-1).

Run:  python3 run.py [--today 2026-07-14]
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "shared"))
import ai
import engine

WINDOW_DAYS = 60
SYSTEM = (pathlib.Path(engine.ROOT / "shared/prompts/filing_notification.md")
          .read_text(encoding="utf-8").split("```")[1].strip())


def template_email(company, filing, fee, days):
    confirm_by = "as soon as possible" if days < 14 else f"within 14 days"
    return f"""Subject: [Action required] {filing['filing_type']} — due {filing['due_date']} — {company['name_en']}

Dear {company['contact_name']},

[template mode] The {filing['description']} for {company['name_en']} is due on
{filing['due_date']} ({days} days from today). Late filing attracts penalties
and higher registration fees.

Our firm can handle this for you: {fee['service_description']}.

Proposed fee: HKD {fee['fee_hkd']}.

Please reply to confirm engagement {confirm_by}, or contact us with any
questions.

Client Services Team
"""


def main():
    today = engine.today()
    print(f"AI provider: {ai.provider()} | run date: {today}\n")
    companies = engine.companies_by_id()
    fees = {f["filing_type"]: f for f in engine.load("fee_schedule.csv")}
    payment_alerts = []

    for filing in engine.load("filings.csv"):
        company = companies[filing["company_id"]]
        days = engine.days_until(filing["due_date"], today)

        if filing["status"] == "payment_due":  # NOA -> time-based payment alerts
            for offset in (14, 7, 1):
                payment_alerts.append({
                    "company": company["name_en"], "filing": filing["description"],
                    "payment_due": filing["due_date"],
                    "alert_date": str(__import__("datetime").date.fromisoformat(filing["due_date"])
                                      - __import__("datetime").timedelta(days=offset)),
                    "channel": company["preferred_channel"],
                    "message": f"Reminder: tax payment for {filing['description']} due {filing['due_date']} (T-{offset})",
                })
            print(f"NOA  {company['name_en']:38s} payment due {filing['due_date']} -> 3 alerts scheduled")
            continue

        if filing["status"] != "pending" or days > WINDOW_DAYS:
            continue

        fee = fees[filing["filing_type"]]
        raw = ai.generate(
            f"Company: {json.dumps(company)}\nFiling: {json.dumps(filing)}\n"
            f"Service & fee: {json.dumps(fee)}\nToday's date: {today}",
            SYSTEM,
        ) or template_email(company, filing, fee, days)
        out = engine.write_text(
            f"filing_notifications/{filing['filing_id']}_{filing['filing_type']}_{company['company_id']}.txt", raw)
        urgency = "OVERDUE" if days < 0 else f"due in {days:3d}d"
        print(f"MAIL {company['name_en']:38s} {filing['filing_type']:5s} {urgency} -> {out.name}")

    if payment_alerts:
        p = engine.save("payment_alerts.csv", payment_alerts)
        print(f"\nPayment alert schedule -> {p.relative_to(engine.ROOT)}")
    print("Human checkpoint: CPA reviews fee and email before anything is sent.")


if __name__ == "__main__":
    main()
