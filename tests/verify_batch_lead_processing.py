from pathlib import Path
import os
import shutil
import stat
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "process_open_leads.sh"
FAKE_PROPOSAL = ROOT / "tests" / "fixtures" / "fake_proposal_lab.sh"
FAKE_GH = ROOT / "tests" / "fixtures" / "fake_gh_batch.sh"
OUTDIR = ROOT / "tmp_batch_output"
CAPTURE_DIR = ROOT / "tmp_batch_capture"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    require(SCRIPT.exists(), "missing tools/process_open_leads.sh")
    FAKE_PROPOSAL.chmod(FAKE_PROPOSAL.stat().st_mode | stat.S_IXUSR)
    FAKE_GH.chmod(FAKE_GH.stat().st_mode | stat.S_IXUSR)

    if OUTDIR.exists():
        shutil.rmtree(OUTDIR)
    if CAPTURE_DIR.exists():
        shutil.rmtree(CAPTURE_DIR)
    OUTDIR.mkdir()

    env = os.environ.copy()
    env["PROPOSAL_LAB_CMD"] = str(FAKE_PROPOSAL)
    env["GH_CMD"] = str(FAKE_GH)
    proc = subprocess.run(
        [str(SCRIPT), str(OUTDIR)],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    require(proc.returncode == 0, f"batch pipeline failed: {proc.stderr or proc.stdout}")

    require((OUTDIR / "11" / "proposal.md").exists(), "open lead without proposal-sent should be processed")
    require(not (OUTDIR / "12").exists(), "lead with proposal-sent should be skipped")
    require((CAPTURE_DIR / "11.md").exists(), "processed lead should receive a comment")
    require((CAPTURE_DIR / "11.label").read_text().strip() == "proposal-sent", "processed lead should get proposal-sent label")

    shutil.rmtree(OUTDIR)
    shutil.rmtree(CAPTURE_DIR)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
