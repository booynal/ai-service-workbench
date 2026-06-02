from pathlib import Path
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "go_now.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    require(SCRIPT.exists(), "missing tools/go_now.py")

    tmp_dir = Path(tempfile.mkdtemp(prefix="go-now-"))
    try:
        out = tmp_dir / "today.md"
        sink = tmp_dir / "clipboard.txt"
        proc = subprocess.run(
            ["python3", str(SCRIPT), str(out), "--pbcopy-cmd", f"cat > {sink}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        require(proc.returncode == 0, f"go_now failed: {proc.stderr or proc.stdout}")
        require(out.exists(), "go_now should render a runbook file")
        require(sink.exists(), "go_now should copy first outreach text to clipboard sink")
        require("我现在开始接三类 AI 代做" in sink.read_text(), "clipboard sink should contain wechat text")
        text = out.read_text()
        require("# Outreach Runbook" in text, "go_now output should contain runbook content")
        stdout = proc.stdout
        require("Preflight check passed." in stdout, "go_now should run preflight first")
        require("Next target: group outreach" in stdout, "go_now should print next target")
        require("today.md" in stdout, "go_now should mention generated runbook path")
        require("Copied text from cn_outreach_packets/微信群首发短文案.txt" in stdout, "go_now should report clipboard copy step")
    finally:
        shutil.rmtree(tmp_dir)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
