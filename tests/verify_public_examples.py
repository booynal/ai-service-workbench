from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    page = ROOT / "docs" / "index.html"
    examples = [
        ROOT / "docs" / "examples.md",
        ROOT / "report_assets" / "sample_proposal.md",
        ROOT / "report_assets" / "report_service_proposal.md",
        ROOT / "report_assets" / "workflow_service_proposal.md",
    ]

    for path in examples:
        require(path.exists(), f"missing public example asset: {path.name}")

    page_text = page.read_text()
    require("./examples.md" in page_text, "public page should link to examples page")
    require("Example Projects" in page_text, "public page should expose examples CTA")

    examples_text = (ROOT / "docs" / "examples.md").read_text()
    require("Automation Script" in examples_text, "examples page missing automation section")
    require("Report Delivery" in examples_text, "examples page missing report section")
    require("AI Workflow Setup" in examples_text, "examples page missing workflow section")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
