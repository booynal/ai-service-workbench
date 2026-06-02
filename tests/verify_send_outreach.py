from pathlib import Path
import os
import shutil
import stat
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "send_github_outreach.py"
FAKE_GH = ROOT / "tests" / "fixtures" / "fake_gh_comment_only.sh"
CAPTURE = ROOT / "tmp_send_capture"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    require(SCRIPT.exists(), "missing tools/send_github_outreach.py")
    FAKE_GH.chmod(FAKE_GH.stat().st_mode | stat.S_IXUSR)

    if CAPTURE.exists():
        shutil.rmtree(CAPTURE)

    env = os.environ.copy()
    env["GH_CMD"] = str(FAKE_GH)

    preview = subprocess.run(
        ["python3", str(SCRIPT), "csa-issue-2"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    require(preview.returncode == 0, f"preview failed: {preview.stderr or preview.stdout}")
    require("PREVIEW ONLY" in preview.stdout, "default mode should be preview only")
    require(not CAPTURE.exists(), "preview mode must not send anything")

    execute = subprocess.run(
        ["python3", str(SCRIPT), "csa-issue-2", "--execute"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    require(execute.returncode == 0, f"execute failed: {execute.stderr or execute.stdout}")
    require(CAPTURE.exists(), "execute mode should send comment")
    require((CAPTURE / "2.md").exists(), "execute mode should comment on issue #2")

    shutil.rmtree(CAPTURE)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
