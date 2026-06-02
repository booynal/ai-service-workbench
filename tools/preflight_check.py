#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    required = [
        "docs/zh.html",
        "runbooks/wechat-group.md",
        "share_assets/wechat-share-card.png",
        "share_assets/zh-landing-qr.png",
        "触达计划.csv",
        "触达日志模板.csv",
        "开始这里-明日执行版.md",
        "最终执行摘要-2026-06-03.md",
    ]

    missing = []
    for rel in required:
        path = ROOT / rel
        if path.exists():
            print(f"PASS {rel}")
        else:
            print(f"FAIL {rel}")
            missing.append(rel)

    if missing:
        print("\nMissing required files:")
        for rel in missing:
            print(f"- {rel}")
        return 1

    print("\nPreflight check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
