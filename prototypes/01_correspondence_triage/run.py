"""Prototype 1 — Incoming correspondence triage.

Reads every letter in data/correspondence/, classifies it (Claude/GPT if an
API key is set, keyword rules otherwise), appends to the correspondence log,
and drafts email + WhatsApp + WeChat notifications for items that need
client attention.

Run:  python3 run.py [--today 2026-07-14]
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "shared"))
import ai
import engine

CLASSIFIER_SYSTEM = (pathlib.Path(engine.ROOT / "shared/prompts/correspondence_classifier.md")
                     .read_text(encoding="utf-8").split("```")[1].strip())
NOTIFIER_SYSTEM = (pathlib.Path(engine.ROOT / "shared/prompts/client_notification.md")
                   .read_text(encoding="utf-8").split("```")[1].strip())

# Keyword fallback so the pipeline still demonstrates end-to-end without a key.
RULES = [
    ("legal_urgent", "urgent", True, r"writ|summons|court|judgment",
     "Legal document received — statutory response window applies"),
    ("statutory_tax", "normal", True, r"inland revenue|profits tax|tax return|assessment",
     "IRD tax correspondence with a filing deadline"),
    ("statutory_cr", "normal", True, r"companies registry|annual return|nar1",
     "Companies Registry statutory filing reminder"),
    ("physical_valuables", "normal", True, r"share certificate|company chop|seal|parcel",
     "Physical valuables received and placed in secure storage"),
    ("marketing_junk", "low", False, r"offer|unsubscribe|discount|% off",
     "Unsolicited marketing material"),
    ("banking", "low", False, r"bank|statement|hsbc|account",
     "Routine bank statement — no action required"),
]

DATE_RE = (r"(\d{1,2} (?:January|February|March|April|May|June|July|August"
           r"|September|October|November|December) \d{4})")


def classify(text: str) -> dict:
    raw = ai.generate(f"Classify this incoming item:\n\n{text}", CLASSIFIER_SYSTEM)
    if raw:
        return json.loads(re.search(r"\{.*\}", raw, re.S).group())
    low = text.lower()
    for category, urgency, notify, pattern, summary in RULES:
        if re.search(pattern, low):
            # ignore the letter's own date line; look for deadlines after it
            deadline = re.findall(DATE_RE, text)
            return {
                "category": category, "urgency": urgency, "notify_client": notify,
                "client_name": _addressee(text), "sender": text.splitlines()[0].title(),
                "summary": f"[template mode] {summary}",
                "deadline": deadline[-1] if len(deadline) > 1 else None,
                "suggested_action": "log and file" if not notify else "notify client and file",
            }
    return {"category": "other", "urgency": "normal", "notify_client": True,
            "client_name": _addressee(text), "sender": "Unknown",
            "summary": "[template mode] unmatched - route to human", "deadline": None,
            "suggested_action": "manual review"}


def _addressee(text: str) -> str:
    m = re.search(r"^([A-Z][A-Z &']+(?:LIMITED|CO\.))\s*$", text, re.M)
    return m.group(1).title() if m else "Unknown"


def draft_notifications(item: dict, client: dict | None) -> str:
    if client:
        raw = ai.generate(
            f"Client record: {json.dumps(client)}\nClassified item: {json.dumps(item)}",
            NOTIFIER_SYSTEM,
        )
        if raw:
            return raw
    name = (client or {}).get("contact_name", "Client")
    deadline = f" Deadline: {item['deadline']}." if item.get("deadline") else ""
    body = (f"We received the following at your registered office today: "
            f"{item['summary']} (from {item['sender']}).{deadline} "
            f"Recommended next step: {item['suggested_action']}.")
    return (f"=== EMAIL ===\nSubject: {'URGENT: ' if item['urgency']=='urgent' else ''}"
            f"Incoming {item['category'].replace('_',' ')} received — action may be required\n"
            f"Dear {name},\n\n{body}\n\nClient Services Team\n"
            f"=== WHATSAPP ===\nHi {name.split()[0]}, {body}\n"
            f"=== WECHAT ===\n[template mode] {body}\n")


def main():
    print(f"AI provider: {ai.provider()}\n")
    clients = {c["name_en"].lower(): c for c in engine.load("companies.csv")}
    log, notified = [], 0

    for path in sorted((engine.DATA / "correspondence").glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        item = classify(text)
        client = clients.get((item.get("client_name") or "").lower())
        log.append({
            "file": path.name, "category": item["category"],
            "client": item.get("client_name") or "-", "urgency": item["urgency"],
            "deadline": item.get("deadline") or "-",
            "notify_client": item["notify_client"], "summary": item["summary"],
            "action": item["suggested_action"],
        })
        flag = "!!" if item["urgency"] == "urgent" else "  "
        print(f"{flag} {path.name:42s} -> {item['category']:18s} notify={item['notify_client']}")

        if item["notify_client"]:
            drafts = draft_notifications(item, client)
            out = engine.write_text(f"notifications/{path.stem}_drafts.txt", drafts)
            notified += 1
            print(f"     drafts -> {out.relative_to(engine.ROOT)}")

    logpath = engine.save("correspondence_log.csv", log)
    print(f"\nLogged {len(log)} items ({notified} client notifications drafted)")
    print(f"Log -> {logpath.relative_to(engine.ROOT)}")
    print("Human checkpoint: review drafts in outputs/notifications/ before sending.")


if __name__ == "__main__":
    main()
