from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    service_form = ROOT / ".github" / "ISSUE_TEMPLATE" / "service-request.yml"
    config_file = ROOT / ".github" / "ISSUE_TEMPLATE" / "config.yml"
    public_page = ROOT / "docs" / "index.html"

    require(service_form.exists(), "missing .github/ISSUE_TEMPLATE/service-request.yml")
    require(config_file.exists(), "missing .github/ISSUE_TEMPLATE/config.yml")

    form_text = service_form.read_text()
    require("name:" in form_text, "service request form missing name")
    require("type: textarea" in form_text, "service request form should collect freeform detail")
    require("type: dropdown" in form_text, "service request form should collect a structured choice")

    config_text = config_file.read_text()
    require("blank_issues_enabled: false" in config_text, "issue chooser should disable blank issues")

    page_text = public_page.read_text()
    require("issues/new/choose" in page_text, "public page should link to issue chooser")
    require("Submit Project Brief" in page_text, "public page should expose a lead-capture CTA")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
