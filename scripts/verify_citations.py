#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from pathlib import Path

repo = Path(__file__).resolve().parents[1]
source_root = (repo / "../octo-cli-source").resolve()
knowledge_root = repo / "knowledge"
log_path = repo / "logs" / "citation-checks.jsonl"
pattern = re.compile(r"来源:\s+`?([^`#\n;]+?)`?#L(\d+)-L(\d+)")
errors = []
checks = 0
for md in sorted(knowledge_root.glob("*.md")):
    text = md.read_text(encoding="utf-8")
    for m in pattern.finditer(text):
        checks += 1
        rel = m.group(1).strip()
        start = int(m.group(2))
        end = int(m.group(3))
        file_path = (source_root / rel).resolve()
        if not str(file_path).startswith(str(source_root)):
            errors.append(f"{md.relative_to(repo)}: path escapes source root: {rel}")
            continue
        if not file_path.exists():
            errors.append(f"{md.relative_to(repo)}: missing file {rel}")
            continue
        lines = file_path.read_text(encoding="utf-8", errors="ignore").splitlines()
        if start < 1 or end > len(lines) or start > end:
            errors.append(f"{md.relative_to(repo)}: invalid lines {rel}#L{start}-L{end} (file has {len(lines)} lines)")
if checks == 0:
    errors.append("no citations found")
record = {
    "time": datetime.now(timezone.utc).isoformat(),
    "checks": checks,
    "status": "failed" if errors else "success",
    "errors": errors,
}
log_path.parent.mkdir(parents=True, exist_ok=True)
with log_path.open("a", encoding="utf-8") as f:
    f.write(json.dumps(record, ensure_ascii=False) + "\n")
if errors:
    print("Citation check failed:")
    print("\n".join(errors))
    raise SystemExit(1)
print(f"All citations valid. checks={checks}")
