from pathlib import Path
import shutil
import stat
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "issue_to_proposal.sh"
ISSUE_FIXTURE = ROOT / "tests" / "fixtures" / "sample_issue.md"
FAKE_PROPOSAL = ROOT / "tests" / "fixtures" / "fake_proposal_lab.sh"
OUTDIR = ROOT / "tmp_pipeline_output"
FAKE_GH = ROOT / "tests" / "fixtures" / "fake_gh.sh"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    require(SCRIPT.exists(), "missing tools/issue_to_proposal.sh")
    FAKE_PROPOSAL.chmod(FAKE_PROPOSAL.stat().st_mode | stat.S_IXUSR)
    FAKE_GH.chmod(FAKE_GH.stat().st_mode | stat.S_IXUSR)

    if OUTDIR.exists():
        shutil.rmtree(OUTDIR)
    OUTDIR.mkdir()

    env = {"PROPOSAL_LAB_CMD": str(FAKE_PROPOSAL)}
    proc = subprocess.run(
        [str(SCRIPT), str(ISSUE_FIXTURE), str(OUTDIR)],
        cwd=ROOT,
        env={**env, **dict()},
        capture_output=True,
        text=True,
    )
    require(proc.returncode == 0, f"pipeline failed: {proc.stderr or proc.stdout}")

    issue_copy = OUTDIR / "issue.md"
    brief_file = OUTDIR / "brief.md"
    proposal_file = OUTDIR / "proposal.md"

    require(issue_copy.exists(), "pipeline should save issue markdown")
    require(brief_file.exists(), "pipeline should create brief.md")
    require(proposal_file.exists(), "pipeline should create proposal.md")

    proposal_text = proposal_file.read_text()
    require("# Fake Proposal" in proposal_text, "fake proposal output missing")
    require("Service type: Automation script" in proposal_text, "brief content should flow into proposal")

    shutil.rmtree(OUTDIR)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
