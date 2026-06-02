from pathlib import Path
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "copy_outreach_text.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    require(SCRIPT.exists(), "missing tools/copy_outreach_text.py")

    tmp_dir = Path(tempfile.mkdtemp(prefix="copy-outreach-"))
    try:
        sink = tmp_dir / "clipboard.txt"
        proc = subprocess.run(
            [
                "python3",
                str(SCRIPT),
                "wechat-group",
                "--pbcopy-cmd",
                f"cat > {sink}",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            shell=False,
        )
        require(proc.returncode == 0, f"copy_outreach_text failed: {proc.stderr or proc.stdout}")
        require(sink.exists(), "clipboard sink file missing")
        text = sink.read_text()
        require("我现在开始接三类 AI 代做" in text, "clipboard should contain wechat outreach text")
        require("微信群首发短文案" in proc.stdout, "stdout should mention source file")
    finally:
        shutil.rmtree(tmp_dir)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
