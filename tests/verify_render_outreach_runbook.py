from pathlib import Path
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "render_outreach_runbook.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    require(SCRIPT.exists(), "missing tools/render_outreach_runbook.py")

    tmp_dir = Path(tempfile.mkdtemp(prefix="runbook-"))
    try:
        out = tmp_dir / "wechat.md"
        proc = subprocess.run(
            ["python3", str(SCRIPT), "wechat-group", str(out)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        require(proc.returncode == 0, f"runbook render failed: {proc.stderr or proc.stdout}")
        require(out.exists(), "runbook output missing")
        text = out.read_text()
        require("# Outreach Runbook" in text, "runbook title missing")
        require("微信群首发短文案" in text, "runbook should include primary message content")
        require("## If Interested" in text, "runbook should include follow-up section")
        require("tools/log_outreach_entry.py" in text, "runbook should include log command")
    finally:
        shutil.rmtree(tmp_dir)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
