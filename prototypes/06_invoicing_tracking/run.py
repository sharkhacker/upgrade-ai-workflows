"""Prototype 6 — Invoicing & payment tracking with AI dunning.

Scans the invoice register: issues new invoices ("draft" -> issue email),
generates stage-appropriate dunning emails for overdue items, and updates
records when payment is confirmed.

Run:   python3 run.py [--today 2026-07-14]
Mark paid:  python3 run.py --mark-paid INV-2026-038 [--today ...]
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "shared"))
import ai
import engine

SYSTEM = (pathlib.Path(engine.ROOT / "shared/prompts/dunning_sequence.md")
          .read_text(encoding="utf-8").split("```")[1].strip())
DUNNING_THRESHOLDS = (1, 15, 30)


def template_email(client, inv, mode, overdue):
    if mode == "issue":
        body = (f"Thank you for your business. Please find invoice {inv['invoice_no']} "
                f"for \"{inv['description']}\" — HKD {inv['amount_hkd']}, due {inv['due_date']}.\n"
                f"Payment: FPS ID 123456789, or cheque payable to the firm.")
        subject = f"Invoice {inv['invoice_no']} — {client['name_en']} — due {inv['due_date']}"
    else:
        stage = int(mode[-1])
        tone = {1: "We believe this is just an oversight —",
                2: f"This is our second notice; the invoice is {overdue} days overdue.",
                3: f"FINAL NOTICE ({overdue} days overdue): ongoing statutory work may be "
                   f"paused and the account escalated. Please respond within 7 days."}[stage]
        body = (f"{tone} invoice {inv['invoice_no']} for \"{inv['description']}\" "
                f"(HKD {inv['amount_hkd']}, due {inv['due_date']}) remains unpaid. "
                f"Please arrange payment or contact us if there is an issue with the invoice.")
        subject = f"Invoice {inv['invoice_no']} — {client['name_en']} — {overdue} days overdue"
    return f"Subject: {subject}\n\nDear {client['contact_name']},\n\n[template mode] {body}\n\nAccounts Team\n"


def dunning_stage(overdue):
    stage = 0
    for i, t in enumerate(DUNNING_THRESHOLDS, 1):
        if overdue >= t:
            stage = i
    return stage


def main():
    today = engine.today()
    invoices = engine.load("invoices.csv")

    if "--mark-paid" in sys.argv:  # payment confirmation -> update records
        target = sys.argv[sys.argv.index("--mark-paid") + 1]
        for inv in invoices:
            if inv["invoice_no"] == target:
                inv["status"], inv["paid_date"] = "paid", str(today)
                engine.save("invoices.csv", invoices, to_data=True)
                print(f"{target} marked paid on {today}; register updated. "
                      f"(Production: receipt email auto-drafted for approval.)")
                return
        sys.exit(f"Invoice {target} not found")

    print(f"AI provider: {ai.provider()} | run date: {today}\n")
    companies = engine.companies_by_id()
    summary = []

    for inv in invoices:
        client = companies[inv["company_id"]]
        overdue = max(0, -engine.days_until(inv["due_date"], today))
        if inv["status"] == "paid":
            print(f"PAID    {inv['invoice_no']}  {client['name_en']:38s} settled {inv['paid_date']}")
            continue
        if inv["status"] == "draft":
            mode = "issue"
        else:
            stage = dunning_stage(overdue)
            if stage == 0:
                print(f"CURRENT {inv['invoice_no']}  {client['name_en']:38s} due {inv['due_date']}")
                continue
            mode = f"dunning stage {stage}"

        raw = ai.generate(
            f"Client: {json.dumps(client)}\nInvoice: {json.dumps(inv)}\n"
            f"Mode: {mode}\nDays overdue: {overdue}\nToday's date: {today}",
            SYSTEM,
        ) or template_email(client, inv, mode, overdue)
        out = engine.write_text(f"invoicing/{inv['invoice_no']}_{mode.replace(' ', '_')}.txt", raw)
        print(f"{'ISSUE' if mode=='issue' else 'DUN-'+mode[-1]:7s} {inv['invoice_no']}  "
              f"{client['name_en']:38s} HKD {inv['amount_hkd']:>6s} -> {out.name}")
        summary.append({"invoice": inv["invoice_no"], "company": client["name_en"],
                        "amount_hkd": inv["amount_hkd"], "action": mode,
                        "days_overdue": overdue})

    if summary:
        p = engine.save("invoicing_actions.csv", summary)
        print(f"\nAction log -> {p.relative_to(engine.ROOT)}")
    print("Human checkpoint: accountant approves all outbound emails; only a human "
          "confirms receipt of payment (--mark-paid).")


if __name__ == "__main__":
    main()
