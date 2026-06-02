from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    runbooks = {
        "wechat": ROOT / "runbooks" / "wechat-group.md",
        "dm": ROOT / "runbooks" / "dm-direct.md",
        "csa": ROOT / "runbooks" / "csa-issue-2.md",
    }

    for name, path in runbooks.items():
        require(path.exists(), f"missing prebuilt runbook: {name}")
        text = path.read_text()
        require("# Outreach Runbook" in text, f"runbook header missing for {name}")

    require("微信群首发短文案" in runbooks["wechat"].read_text(), "wechat runbook should include group message")
    require("一对一私聊首发" in runbooks["dm"].read_text(), "dm runbook should include direct message text")
    require("csa-issue-2" in runbooks["csa"].read_text(), "csa runbook should include candidate key")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
