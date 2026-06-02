from pathlib import Path
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "start_today.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    require(SCRIPT.exists(), "missing tools/start_today.py")

    tmp_dir = Path(tempfile.mkdtemp(prefix="start-today-"))
    try:
        out = tmp_dir / "today-runbook.md"
        proc = subprocess.run(
            ["python3", str(SCRIPT), str(out)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        require(proc.returncode == 0, f"start_today failed: {proc.stderr or proc.stdout}")
        require(out.exists(), "start_today should create a runbook file")
        text = out.read_text()
        require("# Outreach Runbook" in text, "generated runbook should contain runbook content")
        stdout = proc.stdout
        require("group outreach" in stdout, "stdout should mention current top target")
        require("today-runbook.md" in stdout, "stdout should mention output path")
    finally:
        shutil.rmtree(tmp_dir)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
