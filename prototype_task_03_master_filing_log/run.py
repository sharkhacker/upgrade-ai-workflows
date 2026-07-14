"""Prototype 3 — Master filing log with computed deadlines & alerts.

Covers tasks 3 (master filing log) and 8 (annual return deadline tracking).
Builds the master log from first principles — deadlines are COMPUTED from
each company's records using HK statutory rules, not hand-typed:

  NAR1  anniversary of incorporation + 42 days
  56AB  employer's return issued early April, due 1 month later (2 May)
  PTR   block extension by accounting year-end (demo uses 17 Aug for Dec y/e)
  ITR   individual tax returns due early July (demo: 3 Aug with extension)

Then merges known one-off items from filings.csv (e.g. NOAs) and prints an
alert digest for everything inside the alert window.

Run:  python3 run.py [--today 2026-07-14]
"""
import datetime
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "shared"))
import engine

engine.OUT = HERE / "sample_output"

ALERT_WINDOW = 30


def computed_obligations(company, year):
    inc = datetime.date.fromisoformat(company["incorporation_date"])
    anniversary = inc.replace(year=year)
    services = company["services"].split(",")
    obligations = [{
        "filing_type": "NAR1",
        "description": f"Annual Return {year} (anniversary {anniversary})",
        "due_date": str(anniversary + datetime.timedelta(days=42)),
        "rule": "CO s.662: within 42 days of return date",
    }]
    if "payroll" in services:
        obligations.append({
            "filing_type": "56AB", "description": f"Employer's Return {year-1}/{str(year)[2:]}",
            "due_date": f"{year}-05-02", "rule": "IRD: 1 month from 1 Apr issue",
        })
    if "tax" in services:
        obligations.append({
            "filing_type": "PTR", "description": f"Profits Tax Return {year-1}/{str(year)[2:]}",
            "due_date": f"{year}-08-17", "rule": "Block extension, Dec year-end ('D' code)",
        })
    return obligations


def main():
    today = engine.today()
    year = today.year
    # cross-reference the register so already-filed obligations don't alert
    filed = {(f["company_id"], f["filing_type"]) for f in engine.load("filings.csv")
             if f["status"] == "filed"}
    rows = []
    for company in engine.load("companies.csv"):
        for ob in computed_obligations(company, year):
            days = engine.days_until(ob["due_date"], today)
            if (company["company_id"], ob["filing_type"]) in filed:
                status = "filed"
            elif days < 0:
                status = "overdue"
            elif days <= ALERT_WINDOW:
                status = "due_soon"
            else:
                status = "tracked"
            rows.append({
                "company_id": company["company_id"], "company": company["name_en"],
                **ob, "days_remaining": days, "status": status,
            })
    # merge one-off items already in the register (NOAs, ITRs)
    companies = engine.companies_by_id()
    for f in engine.load("filings.csv"):
        if f["filing_type"] in ("NOA", "ITR") and f["status"] in ("pending", "payment_due"):
            days = engine.days_until(f["due_date"], today)
            rows.append({
                "company_id": f["company_id"], "company": companies[f["company_id"]]["name_en"],
                "filing_type": f["filing_type"], "description": f["description"],
                "due_date": f["due_date"], "rule": "from register",
                "days_remaining": days,
                "status": "overdue" if days < 0 else "due_soon" if days <= ALERT_WINDOW else "tracked",
            })

    rows.sort(key=lambda r: r["due_date"])
    path = engine.save("master_filing_log.csv", rows)
    print(f"Master filing log: {len(rows)} obligations across "
          f"{len({r['company_id'] for r in rows})} companies -> {path.relative_to(engine.ROOT)}\n")

    digest = [r for r in rows if r["status"] in ("overdue", "due_soon")]
    print(f"ALERT DIGEST (window = {ALERT_WINDOW} days, run date {today})")
    print("-" * 78)
    for r in digest:
        marker = "OVERDUE " if r["days_remaining"] < 0 else f"T-{r['days_remaining']:<5d} "
        print(f"{marker} {r['due_date']}  {r['filing_type']:5s} {r['company']:38s}")
    body = "\n".join(f"- {r['due_date']} {r['filing_type']} {r['company']} "
                     f"({'OVERDUE' if r['days_remaining']<0 else str(r['days_remaining'])+' days'})"
                     for r in digest)
    out = engine.write_text("alert_digest_email.txt",
        f"Subject: Filing deadline digest — {len(digest)} items need attention ({today})\n\n"
        f"To: company.secretary@firm.example.hk\n\n{body}\n\n— automated daily digest\n")
    print(f"\nDigest email -> {out.relative_to(engine.ROOT)}")
    print("Human checkpoint: secretary validates computed deadlines on first run per company.")


if __name__ == "__main__":
    main()
