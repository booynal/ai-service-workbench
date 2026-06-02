from pathlib import Path
import os
import shutil
import stat
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "pipeline_report.py"
FAKE_GH = ROOT / "tests" / "fixtures" / "fake_gh_report.sh"
OUTDIR = ROOT / "tmp_report_output"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    require(SCRIPT.exists(), "missing tools/pipeline_report.py")
    FAKE_GH.chmod(FAKE_GH.stat().st_mode | stat.S_IXUSR)

    if OUTDIR.exists():
        shutil.rmtree(OUTDIR)
    OUTDIR.mkdir()

    output_file = OUTDIR / "pipeline_report.md"
    env = os.environ.copy()
    env["GH_CMD"] = str(FAKE_GH)
    proc = subprocess.run(
        ["python3", str(SCRIPT), str(output_file)],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    require(proc.returncode == 0, f"report script failed: {proc.stderr or proc.stdout}")
    require(output_file.exists(), "pipeline report file was not created")

    text = output_file.read_text()
    require("# Lead Pipeline Report" in text, "report header missing")
    require("Open leads: 2" in text, "open lead count missing")
    require("Proposal sent: 1" in text, "proposal-sent count missing")
    require("Closed leads: 1" in text, "closed lead count missing")
    require("Lead A" in text and "Lead B" in text and "Lead C" in text, "report should include lead rows")

    shutil.rmtree(OUTDIR)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
