from pathlib import Path
import os
import shutil
import stat
import subprocess


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "tools" / "run_lead_engine.sh"
PLIST = ROOT / "launchd" / "com.booynal.ai-service-workbench.plist"
FAKE_GH = ROOT / "tests" / "fixtures" / "fake_gh_engine.sh"
FAKE_PROPOSAL = ROOT / "tests" / "fixtures" / "fake_proposal_lab.sh"
OUTDIR = ROOT / "tmp_engine_output"
CAPTURE_DIR = ROOT / "tmp_engine_capture"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    require(RUNNER.exists(), "missing tools/run_lead_engine.sh")
    require(PLIST.exists(), "missing launchd/com.booynal.ai-service-workbench.plist")

    FAKE_GH.chmod(FAKE_GH.stat().st_mode | stat.S_IXUSR)
    FAKE_PROPOSAL.chmod(FAKE_PROPOSAL.stat().st_mode | stat.S_IXUSR)
    RUNNER.chmod(RUNNER.stat().st_mode | stat.S_IXUSR)

    if OUTDIR.exists():
        shutil.rmtree(OUTDIR)
    if CAPTURE_DIR.exists():
        shutil.rmtree(CAPTURE_DIR)
    OUTDIR.mkdir()

    env = os.environ.copy()
    env["GH_CMD"] = str(FAKE_GH)
    env["PROPOSAL_LAB_CMD"] = str(FAKE_PROPOSAL)
    proc = subprocess.run(
        [str(RUNNER), str(OUTDIR)],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    require(proc.returncode == 0, f"lead engine failed: {proc.stderr or proc.stdout}")
    require((OUTDIR / "leads" / "31" / "proposal.md").exists(), "runner should process unhandled open lead")
    require((OUTDIR / "pipeline_report.md").exists(), "runner should produce pipeline report")
    require((CAPTURE_DIR / "31.md").exists(), "runner should comment back to processed lead")
    require((CAPTURE_DIR / "31.label").read_text().strip() == "proposal-sent", "runner should mark lead as proposal-sent")

    plist_text = PLIST.read_text()
    require(str(RUNNER) in plist_text, "launchd plist should point to run_lead_engine.sh")

    shutil.rmtree(OUTDIR)
    shutil.rmtree(CAPTURE_DIR)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
