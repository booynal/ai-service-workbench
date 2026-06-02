from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    plan_file = ROOT / "触达计划.csv"
    log_file = ROOT / "触达日志模板.csv"

    require(plan_file.exists(), "missing 触达计划.csv")
    require(log_file.exists(), "missing 触达日志模板.csv")

    plan_text = plan_file.read_text()
    require("csa issue #2" in plan_text, "plan file should keep planned targets")

    log_text = log_file.read_text().strip().splitlines()
    require(len(log_text) == 1, "log template should only contain header")
    require(log_text[0] == "date,channel,target,asset_used,status,next_action,notes", "log template header mismatch")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
