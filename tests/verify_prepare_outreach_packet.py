from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "prepare_outreach_packet.py"
MANIFEST = ROOT / "outreach_packets" / "manifest.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    require(SCRIPT.exists(), "missing tools/prepare_outreach_packet.py")
    require(MANIFEST.exists(), "missing outreach_packets/manifest.json")

    proc = subprocess.run(
        ["python3", str(SCRIPT), "csa-issue-2"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    require(proc.returncode == 0, f"prepare_outreach_packet failed: {proc.stderr or proc.stdout}")
    text = proc.stdout
    require("csa-issue-2" in text, "output should include candidate key")
    require("outreach_packets/csa-issue-2-message.txt" in text, "output should include message path")
    require("outreach_packets/csa-issue-2-proposal.md" in text, "output should include proposal path")
    require("https://github.com/faisalabdullah-commits/csa/issues/2" in text, "output should include target URL")

    proc_cn = subprocess.run(
        ["python3", str(SCRIPT), "wechat-group"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    require(proc_cn.returncode == 0, f"prepare_outreach_packet for chinese packet failed: {proc_cn.stderr or proc_cn.stdout}")
    text_cn = proc_cn.stdout
    require("wechat-group" in text_cn, "output should include chinese packet key")
    require("cn_outreach_packets/微信群首发短文案.txt" in text_cn, "output should include chinese message path")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
