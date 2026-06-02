from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    qr = ROOT / "share_assets" / "zh-landing-qr.png"
    poster = ROOT / "share_assets" / "wechat-share-card.png"

    require(qr.exists(), "missing share_assets/zh-landing-qr.png")
    require(poster.exists(), "missing share_assets/wechat-share-card.png")
    require(qr.stat().st_size > 0, "qr image should not be empty")
    require(poster.stat().st_size > 0, "poster image should not be empty")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
