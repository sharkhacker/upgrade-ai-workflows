"""Shared engine: CSV I/O, date helpers, reminder cadence, output writing.

One engine powers prototypes 3, 4, 5 and 6 — deadline tracking, signing
chasers, change-doc reminders and invoice dunning are all the same pattern:
scan a register, compute days until/past a date, pick an escalation stage,
draft a message, log it.
"""
import csv
import datetime
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"


def load(name: str) -> list[dict]:
    with open(DATA / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save(name: str, rows: list[dict], to_data: bool = False) -> pathlib.Path:
    path = (DATA if to_data else OUT) / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return path


def write_text(relpath: str, text: str) -> pathlib.Path:
    path = OUT / relpath
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def today() -> datetime.date:
    """Run date; override with --today YYYY-MM-DD for reproducible demos."""
    argv = sys.argv
    if "--today" in argv:
        return datetime.date.fromisoformat(argv[argv.index("--today") + 1])
    return datetime.date.today()


def days_until(date_str: str, ref: datetime.date) -> int:
    return (datetime.date.fromisoformat(date_str) - ref).days


def companies_by_id() -> dict[str, dict]:
    return {c["company_id"]: c for c in load("companies.csv")}


def reminder_stage(days_waiting: int, thresholds=(7, 14, 21)) -> int:
    """0 = no reminder yet, 1 = gentle, 2 = firm, 3 = escalate to secretary."""
    stage = 0
    for i, t in enumerate(thresholds, start=1):
        if days_waiting >= t:
            stage = i
    return stage


STAGE_LABEL = {1: "gentle reminder", 2: "firm reminder", 3: "final reminder + internal escalation"}
