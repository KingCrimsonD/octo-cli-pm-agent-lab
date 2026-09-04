#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

REQUIRED = [
    "## 1. 背景", "## 2. 用户目标", "## 3. 目标用户", "## 4. 范围",
    "### 本次包含", "### 本次不包含", "## 5. 用户故事", "## 6. 产品行为",
    "## 7. 验收标准", "## 8. 待确认问题", "## 9. 关联信息",
]
HOW_PATTERNS = [
    r"Redis", r"MySQL", r"PostgreSQL", r"数据库表", r"新增字段", r"接口路径",
    r"HTTP\s*200", r"SQL", r"```", r"函数名", r"类名", r"SDK 实现", r"缓存策略",
    r"消息队列", r"内部字段名", r"API\s*endpoint", r"implementation",
]
SECRET_PATTERNS = [r"github_pat_", r"gh[pousr]_", r"Bearer\s+\S+", r"JSESSIONID=", r"-----BEGIN .*PRIVATE KEY-----"]
USER_VISIBLE_HINTS = ["用户", "看到", "提示", "完成", "知道", "确认", "秒", "失败", "成功"]

def lint(text: str):
    errors = []
    for h in REQUIRED:
        if h not in text:
            errors.append(f"missing required section: {h}")
    for p in HOW_PATTERNS:
        if re.search(p, text, re.I):
            errors.append(f"contains possible How/implementation detail: {p}")
    for p in SECRET_PATTERNS:
        if re.search(p, text, re.I):
            errors.append(f"contains possible secret: {p}")
    acc = text.split("## 7. 验收标准", 1)[1].split("## 8.", 1)[0] if "## 7. 验收标准" in text else ""
    if acc and not any(h in acc for h in USER_VISIBLE_HINTS):
        errors.append("acceptance criteria may not be user-visible")
    if "来源 issue" not in text and "Issue" not in text:
        errors.append("missing linked source issue")
    return errors

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: prd_lint.py <prd.md>", file=sys.stderr)
        raise SystemExit(2)
    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")
    errors = lint(text)
    result = {"file": str(path), "status": "failed" if errors else "success", "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(1 if errors else 0)
