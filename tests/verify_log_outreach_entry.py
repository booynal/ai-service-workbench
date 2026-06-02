from pathlib import Path
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "log_outreach_entry.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    require(SCRIPT.exists(), "missing tools/log_outreach_entry.py")

    tmp_dir = Path(tempfile.mkdtemp(prefix="outreach-log-"))
    try:
        csv_file = tmp_dir / "log.csv"
        csv_file.write_text("date,channel,target,asset_used,status,next_action,notes\n")

        proc = subprocess.run(
            [
                "python3",
                str(SCRIPT),
                str(csv_file),
                "2026-06-03",
                "github",
                "csa issue #2",
                "outreach_packets/csa-issue-2-message.txt",
                "sent",
                "wait 48h",
                "first outbound try",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        require(proc.returncode == 0, f"log_outreach_entry failed: {proc.stderr or proc.stdout}")
        text = csv_file.read_text()
        require("csa issue #2" in text, "target missing from CSV")
        require("outreach_packets/csa-issue-2-message.txt" in text, "asset path missing from CSV")
        require("sent" in text, "status missing from CSV")
    finally:
        shutil.rmtree(tmp_dir)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
