from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    zh_page = ROOT / "docs" / "zh.html"
    group_copy = ROOT / "cn_outreach_packets" / "微信群首发短文案.txt"
    dm_copy = ROOT / "cn_outreach_packets" / "一对一私聊首发.txt"
    english_page = ROOT / "docs" / "index.html"

    require(zh_page.exists(), "missing docs/zh.html")
    zh_text = zh_page.read_text()
    require("AI 代做服务" in zh_text, "zh landing should contain Chinese service positioning")
    require("提交需求" in zh_text, "zh landing should contain issue CTA")
    require("估算价格" in zh_text, "zh landing should contain quote CTA")

    require("/zh.html" in group_copy.read_text(), "wechat packet should point to zh landing page")
    require("/zh.html" in dm_copy.read_text(), "dm packet should point to zh landing page")
    require("./zh.html" in english_page.read_text(), "english landing should link to chinese landing")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
