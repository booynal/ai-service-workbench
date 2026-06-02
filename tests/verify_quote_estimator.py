from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    estimator = ROOT / "docs" / "quote-estimator.html"
    page = ROOT / "docs" / "index.html"

    require(estimator.exists(), "missing docs/quote-estimator.html")

    page_text = page.read_text()
    require("./quote-estimator.html" in page_text, "public page should link to quote estimator")
    require("Estimate Budget" in page_text, "public page should expose quote estimator CTA")

    estimator_text = estimator.read_text()
    require("Service Type" in estimator_text, "quote estimator missing service type input")
    require("Delivery Urgency" in estimator_text, "quote estimator missing urgency input")
    require("Recommended Range" in estimator_text, "quote estimator missing result output")
    require("calcEstimate" in estimator_text, "quote estimator should contain calculation script")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
