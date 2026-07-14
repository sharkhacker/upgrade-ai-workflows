"""Prototype 5 — Change-of-document tracking with bilingual reminders.

Covers task 11 (已提供給客戶未簽回的變更文件): director/secretary changes,
share transfers, registered-office changes, share allotments provided to
clients but not yet signed back. Same escalation engine as prototype 4, but
every reminder is drafted in BOTH English and Traditional Chinese, and the
tone escalates with the stage.

Run:  python3 run.py [--today 2026-07-14]
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "shared"))
import ai
import engine

SYSTEM = (pathlib.Path(engine.ROOT / "shared/prompts/bilingual_change_doc_reminder.md")
          .read_text(encoding="utf-8").split("```")[1].strip())

ZH_DOC = {
    "Share Transfer": "股份轉讓文件",
    "Resignation and Appointment of Director (ND2A)": "董事辭任及委任文件 (ND2A)",
    "Change of Registered Office Address (NR1)": "更改註冊辦事處地址 (NR1)",
    "Share Allotment (NSC1)": "股份配發 (NSC1)",
    "Appointment of Company Secretary (ND2A)": "公司秘書委任文件 (ND2A)",
}


def template_bilingual(client, doc, waiting, stage):
    zh_doc = next((v for k, v in ZH_DOC.items() if k in doc["doc_type"]), doc["doc_type"])
    en_tone = {1: "a friendly reminder", 2: f"our second reminder — outstanding {waiting} days",
               3: "our FINAL reminder — statutory deadlines may be affected"}[stage]
    zh_tone = {1: "友善提示", 2: f"第二次提醒（已逾 {waiting} 天）",
               3: "最後提醒——可能影響法定期限"}[stage]
    return f"""=== ENGLISH ===
Subject: Reminder {stage}: {doc['doc_type']} awaiting signature

Dear {client['contact_name']},

[template mode] This is {en_tone}: the "{doc['doc_type']}" sent on
{doc['sent_date']} has not yet been signed and returned. The related change
cannot be filed with the Companies Registry until we receive it.
{"This matter has been escalated to our company secretary. Please respond within 7 days." if stage == 3 else "Please sign and return at your earliest convenience."}

Client Services Team

=== 中文 ===
主旨：第{stage}次提醒：{zh_doc}尚待簽署

{client['contact_name']} 台鑒：

[template mode] 此乃{zh_tone}：本所於 {doc['sent_date']} 送呈之「{zh_doc}」
尚未簽署交回。在收到已簽署文件前，相關變更無法向公司註冊處提交。
{"此事已轉呈本所公司秘書跟進，敬請於七天內回覆。" if stage == 3 else "敬請儘早簽署及交回。"}

客戶服務部 謹啟
"""


def main():
    today = engine.today()
    print(f"AI provider: {ai.provider()} | run date: {today}\n")
    companies = engine.companies_by_id()
    register, escalations = [], []

    for doc in engine.load("documents_out.csv"):
        if doc["category"] != "change_doc":
            continue
        client = companies[doc["company_id"]]
        waiting = -engine.days_until(doc["sent_date"], today)
        signed = doc["status"] == "signed_returned"
        stage = 0 if signed else engine.reminder_stage(waiting)
        register.append({
            "doc_id": doc["doc_id"], "company": client["name_en"],
            "doc_type": doc["doc_type"], "sent_date": doc["sent_date"],
            "days_outstanding": 0 if signed else waiting,
            "status": doc["status"], "reminder_stage": stage,
            "preferred_channel": client["preferred_channel"], "language": client["language"],
        })
        if signed:
            print(f"OK    {doc['doc_id']} {doc['doc_type'][:52]:54s} signed & returned")
            continue
        if stage == 0:
            print(f"WAIT  {doc['doc_id']} {doc['doc_type'][:52]:54s} {waiting}d — inside grace period")
            continue

        raw = ai.generate(
            f"Client: {json.dumps(client, ensure_ascii=False)}\n"
            f"Document: {json.dumps(doc, ensure_ascii=False)}\n"
            f"Days outstanding: {waiting}\nReminder stage: {stage}\nToday's date: {today}",
            SYSTEM,
        ) or template_bilingual(client, doc, waiting, stage)
        out = engine.write_text(f"change_doc_reminders/{doc['doc_id']}_stage{stage}_bilingual.txt", raw)
        print(f"REMIND {doc['doc_id']} {doc['doc_type'][:52]:53s} {waiting}d stage {stage} -> {out.name}")
        if stage == 3:
            escalations.append(f"- {doc['doc_id']}: {doc['doc_type']} ({client['name_en']}) "
                               f"unsigned {waiting} days")

    engine.save("change_doc_register.csv", register)
    if escalations:
        engine.write_text("change_doc_secretary_escalation.txt",
            "Subject: Change documents unsigned past 21 days\n"
            "To: company.secretary@firm.example.hk\n\n" + "\n".join(escalations) + "\n")
        print(f"\n{len(escalations)} item(s) escalated to company secretary")
    print("Register -> outputs/change_doc_register.csv")
    print("Human checkpoint: secretary approves reminders; channel follows client preference.")


if __name__ == "__main__":
    main()
