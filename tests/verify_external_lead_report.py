from pathlib import Path
import os
import shutil
import stat
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "external_lead_report.sh"
FAKE_GH = ROOT / "tests" / "fixtures" / "fake_gh_lead_search.sh"
FAKE_PROPOSAL = ROOT / "tests" / "fixtures" / "fake_proposal_lab.sh"
OUTDIR = ROOT / "tmp_external_leads"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    require(SCRIPT.exists(), "missing tools/external_lead_report.sh")
    FAKE_GH.chmod(FAKE_GH.stat().st_mode | stat.S_IXUSR)
    FAKE_PROPOSAL.chmod(FAKE_PROPOSAL.stat().st_mode | stat.S_IXUSR)

    if OUTDIR.exists():
        shutil.rmtree(OUTDIR)
    OUTDIR.mkdir()

    env = os.environ.copy()
    env["GH_CMD"] = str(FAKE_GH)
    env["PROPOSAL_LAB_CMD"] = str(FAKE_PROPOSAL)
    proc = subprocess.run(
        [str(SCRIPT), "automation script", str(OUTDIR)],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    require(proc.returncode == 0, f"external lead report failed: {proc.stderr or proc.stdout}")

    report_file = OUTDIR / "lead_report.md"
    proposal_file = OUTDIR / "101" / "proposal.md"
    require(report_file.exists(), "lead report should be created")
    require(proposal_file.exists(), "proposal draft for top lead should be created")

    report_text = report_file.read_text()
    require("example/repo" in report_text, "report should include repository owner/name")
    require("Need automation for support ticket triage" in report_text, "report should include lead title")
    require("https://github.com/example/repo/issues/101" in report_text, "report should include lead URL")

    shutil.rmtree(OUTDIR)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
