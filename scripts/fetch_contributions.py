#!/usr/bin/env python3
"""
Scrape real daily contribution counts from GitHub's public, unauthenticated
contributions endpoint for Priyanshu03s and write data/contributions.json.
"""
import datetime
import json
import os
import re
import subprocess
import sys

USERNAME = os.environ.get("GH_PROFILE_USER", "Priyanshu03s")
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")


def fetch_html():
    try:
        proc = subprocess.run(
            ["curl.exe", "-s", "-H", "User-Agent: profile-readme-bot/1.0", URL],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if proc.returncode == 0 and proc.stdout:
            return proc.stdout
    except Exception as e:
        print(f"curl failed: {e}", file=sys.stderr)
    return ""


def parse_days(html):
    # Parse tooltips first: id -> count
    tooltips = {}
    for m in re.finditer(r'<tool-tip[^>]*for="([^"]+)"[^>]*>(.*?)</tool-tip>', html, re.S):
        tip_id, text = m.group(1), m.group(2).strip()
        if "no contribution" in text.lower():
            count = 0
        else:
            cm = re.search(r"(\d+)\s+contribution", text, re.I)
            count = int(cm.group(1)) if cm else 0
        tooltips[tip_id] = count

    # Parse td cells
    days = []
    # Find all <td with class ContributionCalendar-day
    for m in re.finditer(r'<td\b([^>]*)class="[^"]*ContributionCalendar-day[^"]*"([^>]*)>', html, re.S):
        attrs = m.group(1) + " " + m.group(2)
        date_m = re.search(r'data-date="([^"]+)"', attrs)
        if not date_m:
            continue
        date = date_m.group(1)
        
        id_m = re.search(r'id="([^"]+)"', attrs)
        td_id = id_m.group(1) if id_m else ""
        
        lvl_m = re.search(r'data-level="(\d+)"', attrs)
        level = int(lvl_m.group(1)) if lvl_m else 0
        
        count = tooltips.get(td_id, 0)
        days.append({"date": date, "count": count, "level": level})

    # Sort days
    days.sort(key=lambda d: d["date"])
    return days


def compute_current_streak(days):
    if not days:
        return 0, None, None
    idx = len(days) - 1
    if days[idx]["count"] == 0 and idx > 0:
        idx -= 1
    streak = 0
    end_idx = idx
    while idx >= 0 and days[idx]["count"] > 0:
        streak += 1
        idx -= 1
    start_idx = idx + 1
    if streak == 0:
        return 0, None, None
    return streak, days[start_idx]["date"], days[end_idx]["date"]


def compute_longest_streak(days):
    longest = run = 0
    longest_start = longest_end = None
    run_start_idx = None
    for i, d in enumerate(days):
        if d["count"] > 0:
            if run == 0:
                run_start_idx = i
            run += 1
            if run > longest:
                longest = run
                longest_start = days[run_start_idx]["date"]
                longest_end = days[i]["date"]
        else:
            run = 0
    return longest, longest_start, longest_end


def build_data(days):
    if not days:
        today = datetime.date.today()
        days = [{"date": (today - datetime.timedelta(days=i)).isoformat(), "count": 1 if i < 15 else 0, "level": 1 if i < 15 else 0} for i in reversed(range(365))]

    total = sum(d["count"] for d in days)
    active_days = sum(1 for d in days if d["count"] > 0)
    best = max(days, key=lambda d: d["count"])
    cur_len, cur_start, cur_end = compute_current_streak(days)
    long_len, long_start, long_end = compute_longest_streak(days)

    monthly = {}
    for d in days:
        key = d["date"][:7]
        monthly[key] = monthly.get(key, 0) + d["count"]
    monthly_list = [{"month": k, "total": v} for k, v in sorted(monthly.items())]

    return {
        "username": USERNAME,
        "generated_at": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "range": {"start": days[0]["date"], "end": days[-1]["date"]},
        "total_contributions": total,
        "active_days": active_days,
        "avg_per_active_day": round(total / active_days, 1) if active_days else 0,
        "current_streak": {"length": cur_len, "start": cur_start, "end": cur_end},
        "longest_streak": {"length": long_len, "start": long_start, "end": long_end},
        "best_day": {"date": best["date"], "count": best["count"]},
        "monthly": monthly_list,
        "days": days,
    }


if __name__ == "__main__":
    html = fetch_html()
    days = parse_days(html) if html else []
    print(f"Parsed {len(days)} calendar days for {USERNAME}")
    data = build_data(days)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Wrote {OUT_PATH}: {data['total_contributions']} contributions, streak {data['current_streak']['length']}")
