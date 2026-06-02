from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "today_actions.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    require(SCRIPT.exists(), "missing tools/today_actions.py")
    proc = subprocess.run(
        ["python3", str(SCRIPT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    require(proc.returncode == 0, f"today_actions failed: {proc.stderr or proc.stdout}")
    out = proc.stdout
    require("group outreach" in out, "today actions should mention current top target")
    require("runbooks/wechat-group.md" in out, "today actions should point to the wechat runbook")
    require("触达日志模板.csv" in out, "today actions should mention the log file")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
