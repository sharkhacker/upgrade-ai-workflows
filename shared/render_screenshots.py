"""Render screenshots for every task from real captured content.

Produces three kinds of PNGs into each task's screenshots/ folder:
  - terminal_run.png       — the actual `run.py` terminal session (from
                             screenshots/run_capture.txt, captured live)
  - conversation.png       — the task's real Claude conversation
                             (from prompt_log.md)
  - output_<name>.png      — selected generated files from sample_output/

All content is genuine captured output; this script only renders it to
images (terminal-window style, CJK-aware). Requires Pillow.

    python3 shared/render_screenshots.py
"""
import pathlib
import re
import sys
import unicodedata

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[1]

MONO = "/System/Library/Fonts/Menlo.ttc"
CJK = "/System/Library/Fonts/Hiragino Sans GB.ttc"
SIZE = 22
LINE_H = 34
PAD = 36
WIDTH = 1560
TEXT_W = WIDTH - 2 * PAD

F_MONO = ImageFont.truetype(MONO, SIZE)
F_MONO_B = ImageFont.truetype(MONO, SIZE, index=1)
F_CJK = ImageFont.truetype(CJK, SIZE)

# terminal palette
BG = (24, 26, 32)
FG = (222, 226, 232)
DIM = (130, 138, 150)
GREEN = (135, 205, 120)
YELLOW = (235, 200, 110)
RED = (240, 120, 110)
CYAN = (120, 200, 230)
BAR = (46, 50, 60)


def is_cjk(ch: str) -> bool:
    return unicodedata.east_asian_width(ch) in ("W", "F")


def seg_runs(text: str):
    """Split a line into (font, chunk) runs so CJK renders with a CJK font."""
    runs, cur, cur_cjk = [], "", None
    for ch in text:
        c = is_cjk(ch)
        if cur_cjk is None or c == cur_cjk:
            cur += ch
        else:
            runs.append((cur_cjk, cur))
            cur = ch
        cur_cjk = c
    if cur:
        runs.append((cur_cjk, cur))
    return runs


def text_width(draw, text, bold=False):
    w = 0
    for cjk, chunk in seg_runs(text):
        font = F_CJK if cjk else (F_MONO_B if bold else F_MONO)
        w += draw.textlength(chunk, font=font)
    return w


def draw_line(draw, x, y, text, fill, bold=False):
    for cjk, chunk in seg_runs(text):
        font = F_CJK if cjk else (F_MONO_B if bold else F_MONO)
        draw.text((x, y), chunk, font=font, fill=fill)
        x += draw.textlength(chunk, font=font)


def wrap(draw, text, indent=0):
    """Wrap a line to TEXT_W, preserving leading whitespace on continuations."""
    if not text:
        return [""]
    out, cur = [], ""
    for ch in text:
        if text_width(draw, cur + ch) > TEXT_W - indent:
            out.append(cur)
            cur = "  " + ch.lstrip() if not is_cjk(ch) else "  " + ch
        else:
            cur += ch
    out.append(cur)
    return out


def color_for(line: str):
    if re.search(r"OVERDUE|FINAL|URGENT|!!|\bDUN-3\b", line):
        return RED
    if re.search(r"^\$ ", line):
        return GREEN
    if re.search(r"Human checkpoint|provider|Register ->|Log ->|Digest email|drafts ->|Action log|alert schedule|escalation ->", line):
        return YELLOW
    if re.search(r"^(MAIL|NOA|CHASE|REMIND|ISSUE|PAID|OK|WAIT|DUN|CURRENT|T-\d)", line):
        return CYAN
    return FG


def render_window(lines_with_style, title, out_path):
    """lines_with_style: list of (text, fill, bold)."""
    dummy = Image.new("RGB", (10, 10))
    ddraw = ImageDraw.Draw(dummy)
    flat = []
    for text, fill, bold in lines_with_style:
        for i, seg in enumerate(wrap(ddraw, text)):
            flat.append((seg, fill, bold))

    header_h = 64
    height = header_h + PAD + LINE_H * len(flat) + PAD
    img = Image.new("RGB", (WIDTH, height), BG)
    draw = ImageDraw.Draw(img)

    # macOS-style title bar
    draw.rectangle([0, 0, WIDTH, header_h], fill=BAR)
    for i, c in enumerate([(255, 96, 88), (255, 189, 46), (39, 201, 63)]):
        draw.ellipse([24 + i * 34, 22, 44 + i * 34, 42], fill=c)
    tw = text_width(draw, title)
    draw_line(draw, (WIDTH - tw) / 2, 18, title, DIM)

    y = header_h + PAD
    for text, fill, bold in flat:
        draw_line(draw, PAD, y, text, fill if fill else color_for(text), bold)
        y += LINE_H
    img.save(out_path)
    print(f"  -> {out_path.relative_to(ROOT)}")


def render_terminal(capture: pathlib.Path, title: str, out: pathlib.Path):
    lines = capture.read_text(encoding="utf-8").rstrip().splitlines()
    styled = [(ln, None, ln.startswith("$ ")) for ln in lines]
    render_window(styled, title, out)


def render_conversation(log: pathlib.Path, title: str, out: pathlib.Path):
    """Render prompt_log.md as a Claude Code-style session."""
    text = log.read_text(encoding="utf-8")
    styled = [("claude  (Claude Code CLI - print mode, Bedrock)", DIM, False), ("", None, False)]
    sections = re.split(r"^### ", text, flags=re.M)
    for sec in sections[1:]:
        head, _, body = sec.partition("\n")
        body = re.sub(r"^```\w*\n?|```\s*$", "", body.strip(), flags=re.M).strip()
        body = re.sub(r"\n?---\s*$", "", body).strip()
        if head.startswith("System prompt"):
            styled.append(("[system prompt]", GREEN, True))
        elif head.startswith("User message"):
            styled.append(("> user", CYAN, True))
        else:
            styled.append(("* claude", YELLOW, True))
        for ln in body.splitlines():
            styled.append(("  " + ln, FG if not head.startswith("Claude") else (235, 238, 245), False))
        styled.append(("", None, False))
    render_window(styled, title, out)


def render_document(src: pathlib.Path, title: str, out: pathlib.Path):
    lines = src.read_text(encoding="utf-8").rstrip().splitlines()
    styled = []
    for ln in lines:
        if ln.startswith("===") or ln.startswith("**Subject") or ln.startswith("Subject"):
            styled.append((ln, YELLOW, True))
        else:
            styled.append((ln, FG, False))
    render_window(styled, title, out)


PROTOS = {
    "prototype_task_01_correspondence_triage": [
        ("doc", "sample_output/notifications/letter_05_court_summons_drafts.txt",
         "output — court summons: email + WhatsApp + WeChat drafts"),
    ],
    "prototype_task_02_filing_notifications": [
        ("doc", "sample_output/filing_notifications/F005_56AB_C005.txt",
         "output — 56AB notification (client language: zh)"),
    ],
    "prototype_task_03_master_filing_log": [
        ("doc", "sample_output/alert_digest_email.txt",
         "output — daily digest email to company secretary"),
    ],
    "prototype_task_07_doc_distribution_tracking": [
        ("doc", "sample_output/chasers/D002_stage1.txt",
         "output — stage 1 chaser draft"),
    ],
    "prototype_task_11_change_doc_reminders": [
        ("doc", "sample_output/change_doc_reminders/D005_stage3_bilingual.txt",
         "output — stage 3 bilingual reminder (EN + 繁體中文)"),
    ],
    "prototype_task_12_invoicing_payment_tracking": [
        ("doc", "sample_output/invoicing/INV-2026-035_dunning_stage_2.txt",
         "output — dunning stage 2 email"),
    ],
}

DESIGN_ONLY = [
    "task_04_company_incorporation_support",
    "task_05_cdd_search",
    "task_06_incorporation_document_prep",
    "task_09_annual_return_preparation",
]


def main():
    for folder, docs in PROTOS.items():
        fdir = ROOT / folder
        sdir = fdir / "screenshots"
        sdir.mkdir(exist_ok=True)
        print(f"{folder}:")
        cap = sdir / "run_capture.txt"
        if cap.exists():
            render_terminal(cap, f"{folder} — python3 run.py", sdir / "terminal_run.png")
        extra = sdir / "run_capture_markpaid.txt"
        if extra.exists():
            render_terminal(extra, f"{folder} — mark-paid flow", sdir / "terminal_markpaid.png")
        log = fdir / "prompt_log.md"
        if log.exists():
            render_conversation(log, f"claude — {folder}", sdir / "conversation.png")
        for kind, rel, title in docs:
            render_document(fdir / rel, title, sdir / f"output_{pathlib.Path(rel).stem}.png")

    for folder in DESIGN_ONLY:
        fdir = ROOT / folder
        sdir = fdir / "screenshots"
        sdir.mkdir(exist_ok=True)
        print(f"{folder}:")
        render_conversation(fdir / "prompt_log.md", f"claude — {folder}", sdir / "conversation.png")

    print("DONE")


if __name__ == "__main__":
    main()
