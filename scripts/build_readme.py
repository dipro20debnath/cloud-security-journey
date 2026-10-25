#!/usr/bin/env python3
"""Regenerate README.md from the progress data in progress/*.json.

Edit the JSON files, then run:  python3 scripts/build_readme.py
"""
import datetime
import json
import pathlib
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "progress"
LOGS = ROOT / "logs"
PLANNED_HOURS_PER_DAY = 2.5

STATUS_ICON = {"done": "🟩", "in_progress": "🟨", "todo": "⬜"}
STATUS_TEXT = {"done": "done", "in_progress": "in progress", "todo": "to do"}
DOW = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def load(name):
    return json.loads((DATA / f"{name}.json").read_text(encoding="utf-8"))


def date(s):
    return datetime.date.fromisoformat(s)


def fmt_date(s):
    d = date(s)
    return f"{d.day} {d:%b %Y}"


def fmt_num(x):
    return f"{x:g}"


def pct(a, b):
    return 0 if not b else a / b


def bar(share, width=10):
    filled = round(max(0, min(1, share)) * width)
    return "█" * filled + "░" * (width - filled)


def badge(label, message, color):
    esc = lambda s: urllib.parse.quote(s.replace("-", "--").replace("_", "__"), safe="")
    return f"![{label}](https://img.shields.io/badge/{esc(label)}-{esc(message)}-{color})"


def mermaid_safe(text):
    return text.replace(":", " -").replace("#", "").replace(";", ",")


def log_path(day):
    return LOGS / f"day-{day:02d}.md"


def main():
    daily = sorted(load("daily"), key=lambda d: d["day"])
    phases = sorted(load("phases"), key=lambda p: p["phase"])
    milestones = sorted(load("milestones"), key=lambda m: m["date"])
    gates = [g for g in load("gates") if g["gate"] == "Gate 1"]
    metrics = load("metrics")

    total = len(daily)
    done = sum(1 for d in daily if d["status"] == "done")
    hours = sum(float(d.get("hours") or 0) for d in daily)
    planned_hours = total * PLANNED_HOURS_PER_DAY
    open_days = [d for d in daily if d["status"] != "done"]
    current = next((d for d in open_days if d["status"] == "in_progress"), open_days[0] if open_days else None)
    next_ms = next((m for m in milestones if m["status"] != "done"), None)
    gate_done = sum(1 for g in gates if g["status"] == "done")

    for p in phases:
        if p["phase"] == 1:
            p["progress"] = pct(done, total)
    current_phase = next((p for p in phases if p["progress"] < 1), phases[-1])

    today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=6))).date()
    out = []
    w = out.append

    # Header
    w("# Cloud Security Journey")
    w("")
    w("> From fundamentals to a global Cloud Security Engineer role, learning in public one day at a time.")
    w("")
    w("**Dipro** · CSE student at Metropolitan University, Sylhet, Bangladesh  ")
    w("Focus: AWS · Cloud security · DevSecOps")
    w("")
    w(" ".join([
        badge("phase", f"{current_phase['phase']} {current_phase['name']}", "blue"),
        badge("days done", f"{done}/{total}", "2ea44f" if done else "lightgrey"),
        badge("hours", fmt_num(hours), "informational"),
        badge("Gate 1", f"{gate_done}/{len(gates)}", "2ea44f" if gate_done == len(gates) else "lightgrey"),
    ]))
    w("")
    w(f"_Last updated {today.day} {today:%b %Y}._")
    w("")

    # Now
    w("## Now")
    w("")
    if current:
        w(f"- **Current:** Day {current['day']} · {current['topic']} ({STATUS_TEXT[current['status']]})")
    else:
        w("- **Current:** Phase 1 complete")
    w(f"- **Phase 1:** {done} of {total} days complete ({pct(done, total):.0%})")
    if next_ms:
        w(f"- **Next milestone:** {fmt_date(next_ms['date'])} · {next_ms['event']}")
    w("")

    # At a glance
    w("## At a glance")
    w("")
    w("| Metric | Done | Target | Progress |")
    w("| --- | ---: | ---: | --- |")
    w(f"| Phase 1 days complete | {done} | {total} | `{bar(pct(done, total))}` {pct(done, total):.0%} |")
    w(f"| Hours logged | {fmt_num(hours)} | {fmt_num(planned_hours)} | `{bar(pct(hours, planned_hours))}` {pct(hours, planned_hours):.0%} |")
    w(f"| Gate 1 criteria met | {gate_done} | {len(gates)} | `{bar(pct(gate_done, len(gates)))}` {pct(gate_done, len(gates)):.0%} |")
    for m in metrics:
        share = pct(m["current"], m["target"])
        w(f"| {m['label']} | {fmt_num(m['current'])} | {fmt_num(m['target'])} | `{bar(share)}` {share:.0%} |")
    w("")

    # Roadmap
    w("## Roadmap")
    w("")
    w("| Phase | Dates | Focus | Gate to pass | Progress |")
    w("| --- | --- | --- | --- | --- |")
    for p in phases:
        w(f"| {p['phase']}. {p['name']} | {fmt_date(p['start'])} – {fmt_date(p['end'])} | {p['goal']} | {p['gate']} | {p['progress']:.0%} |")
    w("")
    w("```mermaid")
    w("gantt")
    w("    title Cloud security roadmap")
    w("    dateFormat YYYY-MM-DD")
    w("    axisFormat %b %Y")
    for p in phases:
        w(f"    section Phase {p['phase']}")
        tag = "done, " if p["progress"] >= 1 else ("active, " if p is current_phase else "")
        w(f"    {mermaid_safe(p['name'])} :{tag}p{p['phase']}, {p['start']}, {p['end']}")
        for m in milestones:
            if m["phase"] == p["phase"] and m["kind"] != "Community":
                mtag = "done, milestone" if m["status"] == "done" else "milestone"
                w(f"    {mermaid_safe(m['event'])} :{mtag}, {m['id']}, {m['date']}, 0d")
    w("```")
    w("")

    # Phase 1 daily grid
    w("## Phase 1 · daily progress")
    w("")
    w("🟩 done · 🟨 in progress · ⬜ to do · ⭐ community event")
    w("")
    w("| Week | " + " | ".join(DOW) + " | Done | Focus |")
    w("| --- | " + " | ".join([":-:"] * 7) + " | ---: | --- |")
    for wk in sorted({d["week"] for d in daily}):
        days = [d for d in daily if d["week"] == wk]
        cells = []
        for d in days:
            cell = f"{STATUS_ICON[d['status']]} {d['day']}"
            if d["event"]:
                cell += " ⭐"
            if log_path(d["day"]).exists():
                cell = f"[{cell}](logs/day-{d['day']:02d}.md)"
            cells.append(cell)
        wdone = sum(1 for d in days if d["status"] == "done")
        w(f"| W{wk} | " + " | ".join(cells) + f" | {wdone}/{len(days)} | {days[0]['week_title']} |")
    w("")

    # This week
    if current:
        wk = current["week"]
        w(f"### This week · W{wk} · {current['week_title']}")
        w("")
        w("| Day | Date | Topic | Status | Log |")
        w("| ---: | --- | --- | --- | --- |")
        for d in [x for x in daily if x["week"] == wk]:
            topic = d["topic"] + (f" · ⭐ {d['event']}" if d["event"] else "")
            log = f"[day-{d['day']:02d}](logs/day-{d['day']:02d}.md)" if log_path(d["day"]).exists() else "—"
            w(f"| {d['day']} | {fmt_date(d['planned_date'])} | {topic} | {STATUS_ICON[d['status']]} {STATUS_TEXT[d['status']]} | {log} |")
        w("")

    # Gate 1
    w("## Gate 1 checklist")
    w("")
    w("All of these must be true before Phase 2 starts.")
    w("")
    for g in gates:
        w(f"- [{'x' if g['status'] == 'done' else ' '}] {g['item']}")
    w("")

    # Milestones
    w("## Milestones")
    w("")
    w("| Date | Milestone | Type | Status |")
    w("| --- | --- | --- | --- |")
    for m in milestones:
        w(f"| {fmt_date(m['date'])} | {m['event']} | {m['kind']} | {'✅ done' if m['status'] == 'done' else '⏳ upcoming'} |")
    w("")

    # Logs
    w("## Daily logs")
    w("")
    logged = [d for d in daily if log_path(d["day"]).exists()]
    if logged:
        for d in logged:
            w(f"- [Day {d['day']:02d} · {d['topic']}](logs/day-{d['day']:02d}.md)")
    else:
        w("_No logs yet. Day 1 is in progress._")
    w("")

    # Structure
    w("## Repository structure")
    w("")
    w("```text")
    w("cloud-security-journey/")
    w("├── README.md              # this dashboard (generated)")
    w("├── logs/                  # one learning log per day: day-01.md, day-02.md, ...")
    w("├── progress/              # progress data the dashboard is built from")
    w("└── scripts/")
    w("    └── build_readme.py    # regenerates README.md from progress/")
    w("```")
    w("")
    w("This README is generated from `progress/*.json` by `scripts/build_readme.py`. "
      "To update it, edit the data and run `python3 scripts/build_readme.py`.")
    w("")

    (ROOT / "README.md").write_text("\n".join(out), encoding="utf-8")
    print(f"README.md written: day {current['day'] if current else '-'} current, {done}/{total} done")


if __name__ == "__main__":
    main()
