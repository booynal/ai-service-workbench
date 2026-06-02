from pathlib import Path
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "next_outreach.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    require(SCRIPT.exists(), "missing tools/next_outreach.py")

    tmp_dir = Path(tempfile.mkdtemp(prefix="next-outreach-"))
    try:
        plan = tmp_dir / "plan.csv"
        log = tmp_dir / "log.csv"

        plan.write_text(
            "date,channel,target,asset_used,status,next_action,notes\n"
            "2026-06-03,github,csa issue #2,outreach_packets/csa-issue-2-message.txt,drafted,send short probe first,highest-priority outbound candidate\n"
            "2026-06-03,wechat,group outreach,cn_outreach_packets/微信群首发短文案.txt,drafted,send first batch,highest-priority local channel\n"
        )
        log.write_text("date,channel,target,asset_used,status,next_action,notes\n")

        proc = subprocess.run(
            ["python3", str(SCRIPT), str(plan), str(log)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        require(proc.returncode == 0, f"next_outreach failed: {proc.stderr or proc.stdout}")
        out = proc.stdout
        require("group outreach" in out, "should recommend first outstanding planned target")
        require("cn_outreach_packets/微信群首发短文案.txt" in out, "should include asset path")

        log.write_text(
            "date,channel,target,asset_used,status,next_action,notes\n"
            "2026-06-03,wechat,group outreach,cn_outreach_packets/微信群首发短文案.txt,sent,wait reply,done\n"
        )
        proc2 = subprocess.run(
            ["python3", str(SCRIPT), str(plan), str(log)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        require(proc2.returncode == 0, f"next_outreach second call failed: {proc2.stderr or proc2.stdout}")
        out2 = proc2.stdout
        require("csa issue #2" in out2, "after logging sent outreach, should recommend the next target")
    finally:
        shutil.rmtree(tmp_dir)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
