from pathlib import Path
import shutil
import stat
import subprocess
import os


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "issue_to_proposal.sh"
FAKE_PROPOSAL = ROOT / "tests" / "fixtures" / "fake_proposal_lab.sh"
FAKE_GH = ROOT / "tests" / "fixtures" / "fake_gh.sh"
OUTDIR = ROOT / "tmp_pipeline_remote_output"


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

    env = os.environ.copy()
    env["PROPOSAL_LAB_CMD"] = str(FAKE_PROPOSAL)
    env["GH_CMD"] = str(FAKE_GH)
    proc = subprocess.run(
        [str(SCRIPT), "123", str(OUTDIR)],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    require(proc.returncode == 0, f"remote pipeline failed: {proc.stderr or proc.stdout}")

    issue_copy = OUTDIR / "issue.md"
    proposal_file = OUTDIR / "proposal.md"
    require(issue_copy.exists(), "remote pipeline should fetch and save issue markdown")
    require(proposal_file.exists(), "remote pipeline should produce proposal")
    require("### Service type" in issue_copy.read_text(), "fetched issue markdown should come from gh output")

    shutil.rmtree(OUTDIR)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
