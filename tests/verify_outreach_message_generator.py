from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "generate_outreach_message.py"
INPUT = ROOT / "tmp_live_candidate_2.md"
OUTDIR = ROOT / "tmp_outreach_message"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    require(SCRIPT.exists(), "missing tools/generate_outreach_message.py")

    if OUTDIR.exists():
        for child in OUTDIR.iterdir():
            child.unlink()
    else:
        OUTDIR.mkdir()

    output_file = OUTDIR / "message.txt"
    proc = subprocess.run(
        ["python3", str(SCRIPT), str(INPUT), str(output_file)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    require(proc.returncode == 0, f"outreach generator failed: {proc.stderr or proc.stdout}")
    require(output_file.exists(), "outreach message file not created")

    text = output_file.read_text()
    require("Hi," in text, "message should start with a greeting")
    require("workflow" in text.lower(), "message should reflect workflow context")
    require("short" in text.lower() or "concise" in text.lower(), "message should position itself as lightweight")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
