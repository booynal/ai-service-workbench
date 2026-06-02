from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "preflight_check.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    require(SCRIPT.exists(), "missing tools/preflight_check.py")

    proc = subprocess.run(
        ["python3", str(SCRIPT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    require(proc.returncode == 0, f"preflight_check failed: {proc.stderr or proc.stdout}")
    out = proc.stdout
    require("PASS" in out, "preflight should report passing checks")
    require("docs/zh.html" in out, "preflight should check chinese landing page file")
    require("runbooks/wechat-group.md" in out, "preflight should check main runbook")
    require("share_assets/wechat-share-card.png" in out, "preflight should check share asset")
    require("触达计划.csv" in out, "preflight should check outreach plan")
    require("触达日志模板.csv" in out, "preflight should check log template")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
