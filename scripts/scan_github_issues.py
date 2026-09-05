#!/usr/bin/env python3
"""Scan demand-pool GitHub issues and write idempotent audit logs.

This script is intentionally conservative: it never prints or logs secret values,
and it only writes local JSONL/state by default. If GH_TOKEN/GITHUB_TOKEN and
DEMAND_REPO are configured, it reads issue metadata via GitHub REST API.

Required env for real scanning:
  DEMAND_REPO=owner/repo
Optional:
  GITHUB_TOKEN or GH_TOKEN
  EXAM_GROUP_TARGET=group:<groupId>
  EXAMINER_MENTION=@[uid:displayName]

Group sending is not performed directly here; OpenClaw channel delivery should
be handled by the agent/runtime after reviewing sync-events.jsonl.
"""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOGS = ROOT / "logs"
STATE = ROOT / "state"
PROCESSED = STATE / "processed_events.json"
SNAPSHOT = STATE / "issue_snapshot.json"
CRON_LOG = LOGS / "cron-runs.jsonl"
SYNC_LOG = LOGS / "sync-events.jsonl"
ACTION_LOG = LOGS / "agent-actions.jsonl"

SECRET_HINTS = ("ghp_", "github_pat_", "Bearer ", "token=", "access_token=", "api_key=", "secret=", "cookie", "JSESSIONID", "private key", "octo token")


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def append_jsonl(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.open("a", encoding="utf-8").write(json.dumps(record, ensure_ascii=False) + "\n")


def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def save_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def redacted_headers(token: str | None) -> dict:
    h = {"Accept": "application/vnd.github+json", "User-Agent": "octo-cli-product-steward"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def github_get(url: str, token: str | None):
    req = urllib.request.Request(url, headers=redacted_headers(token))
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.loads(resp.read().decode("utf-8"))


def issue_fingerprint(issue: dict) -> str:
    payload = {
        "number": issue.get("number"),
        "title": issue.get("title"),
        "state": issue.get("state"),
        "state_reason": issue.get("state_reason"),
        "labels": sorted([l.get("name", "") for l in issue.get("labels", [])]),
        "updated_at": issue.get("updated_at"),
        "comments": issue.get("comments"),
        "assignees": sorted([a.get("login", "") for a in issue.get("assignees", [])]),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


REPORT_EVENTS = {
    "new-issue",
    "pm-needs-prd",
    "pm-prd-created",
    "pm-review-passed",
    "pm-review-failed",
    "status-in-review",
    "status-changes-requested",
    "status-ready",
    "status-need-human",
    "closed-wontfix",
}


def classify_event(issue: dict, previous: dict | None) -> list[str]:
    labels = {l.get("name", "") for l in issue.get("labels", [])}
    prev_labels = set(previous.get("labels", [])) if previous else set()
    events = []
    if previous is None:
        events.append("new-issue")
    else:
        if issue.get("title") != previous.get("title"):
            events.append("title-changed")
        if issue.get("state") != previous.get("state"):
            events.append("state-changed")
        if labels != prev_labels:
            events.append("labels-changed")
        if issue.get("comments") != previous.get("comments"):
            events.append("comments-changed")
        if issue.get("updated_at") != previous.get("updated_at") and not events:
            events.append("body-or-metadata-changed")

    # Emit explicit PM/status milestones only when newly observed. These are the
    # events that can justify a group report; generic labels-changed remains an
    # audit event but is intentionally quiet.
    label_events = {
        "pm:needs-prd": "pm-needs-prd",
        "pm:prd-created": "pm-prd-created",
        "pm:review-passed": "pm-review-passed",
        "pm:review-failed": "pm-review-failed",
        "status:in-review": "status-in-review",
        "status:changes-requested": "status-changes-requested",
        "status:ready": "status-ready",
        "status:need-human": "status-need-human",
    }
    for label, event in label_events.items():
        if label in labels and label not in prev_labels:
            events.append(event)

    if issue.get("state") == "closed" and issue.get("state_reason") == "not_planned":
        events.append("closed-wontfix")
    return sorted(set(events))


def main() -> int:
    repo = os.getenv("DEMAND_REPO", "").strip()
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    started = now()
    if not repo:
        append_jsonl(CRON_LOG, {"ts": started, "status": "skipped", "reason": "DEMAND_REPO not configured"})
        print("Skipped: DEMAND_REPO not configured")
        return 0

    processed = load_json(PROCESSED, {})
    snapshot = load_json(SNAPSHOT, {})
    new_snapshot = {}
    emitted = 0
    try:
        issues = github_get(f"https://api.github.com/repos/{repo}/issues?state=all&per_page=100", token)
        for issue in issues:
            if "pull_request" in issue:
                continue
            number = str(issue.get("number"))
            labels = sorted([l.get("name", "") for l in issue.get("labels", [])])
            current = {
                "number": issue.get("number"),
                "title": issue.get("title"),
                "state": issue.get("state"),
                "state_reason": issue.get("state_reason"),
                "labels": labels,
                "updated_at": issue.get("updated_at"),
                "comments": issue.get("comments"),
                "assignees": sorted([a.get("login", "") for a in issue.get("assignees", [])]),
                "html_url": issue.get("html_url"),
                "fingerprint": issue_fingerprint(issue),
            }
            previous = snapshot.get(number)
            new_snapshot[number] = current
            if previous and previous.get("fingerprint") == current["fingerprint"]:
                continue
            for ev in classify_event(issue, previous):
                key = f"issue-{number}-{ev}-{issue.get('updated_at')}"
                if processed.get(key):
                    continue
                processed[key] = True
                event = {"ts": now(), "repo": repo, "event_key": key, "event": ev, "issue_number": issue.get("number"), "title": issue.get("title"), "url": issue.get("html_url"), "labels": labels, "state": issue.get("state"), "state_reason": issue.get("state_reason"), "group_report_needed": ev in REPORT_EVENTS}
                append_jsonl(SYNC_LOG, event)
                emitted += 1
        save_json(SNAPSHOT, new_snapshot)
        save_json(PROCESSED, processed)
        append_jsonl(CRON_LOG, {"ts": started, "status": "ok", "repo": repo, "issues_seen": len(new_snapshot), "events_emitted": emitted})
        print(f"OK: issues_seen={len(new_snapshot)} events_emitted={emitted}")
        return 0
    except urllib.error.HTTPError as e:
        status = "github-http-error"
        detail = f"HTTP {e.code}"
    except Exception as e:
        status = "error"
        detail = type(e).__name__
    append_jsonl(CRON_LOG, {"ts": started, "status": status, "repo": repo, "detail": detail})
    append_jsonl(ACTION_LOG, {"ts": now(), "action": "need-human", "reason": f"GitHub scan failed: {detail}", "labels": ["status:need-human"]})
    print(f"Failed: {detail}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
