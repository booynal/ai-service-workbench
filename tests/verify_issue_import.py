from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "sample_issue.md"
SCRIPT = ROOT / "tools" / "issue_to_brief.py"
OUTDIR = ROOT / "tmp_test_output"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    require(SCRIPT.exists(), "missing tools/issue_to_brief.py")
    if OUTDIR.exists():
      shutil.rmtree(OUTDIR)
    OUTDIR.mkdir()

    output_file = OUTDIR / "brief.md"
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), str(FIXTURE), str(output_file)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    require(proc.returncode == 0, f"import script failed: {proc.stderr or proc.stdout}")
    require(output_file.exists(), "brief output file was not created")

    text = output_file.read_text()
    require("# Imported Service Request" in text, "brief title missing")
    require("Service type: Automation script" in text, "service type missing")
    require("Budget range: 1000-3000 CNY" in text, "budget missing")
    require("Local-only processing." in text, "constraints missing")

    shutil.rmtree(OUTDIR)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
