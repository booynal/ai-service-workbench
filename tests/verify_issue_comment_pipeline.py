from pathlib import Path
import os
import shutil
import stat
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "issue_to_proposal_and_comment.sh"
FAKE_PROPOSAL = ROOT / "tests" / "fixtures" / "fake_proposal_lab.sh"
FAKE_GH = ROOT / "tests" / "fixtures" / "fake_gh_issue_comment.sh"
OUTDIR = ROOT / "tmp_comment_pipeline_output"
CAPTURE_DIR = ROOT / "tmp_comment_capture"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    require(SCRIPT.exists(), "missing tools/issue_to_proposal_and_comment.sh")
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
        [str(SCRIPT), "9", str(OUTDIR)],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    require(proc.returncode == 0, f"comment pipeline failed: {proc.stderr or proc.stdout}")

    proposal_file = OUTDIR / "proposal.md"
    comment_file = CAPTURE_DIR / "9.md"
    require(proposal_file.exists(), "proposal file missing")
    require(comment_file.exists(), "issue comment body should be captured")
    require("# Fake Proposal" in comment_file.read_text(), "comment should contain proposal body")

    shutil.rmtree(OUTDIR)
    shutil.rmtree(CAPTURE_DIR)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
