#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import qrcode
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "share_assets"
URL = "https://booynal.github.io/ai-service-workbench/zh.html"


def make_qr(path: Path) -> None:
    img = qrcode.make(URL)
    img.save(path)


def load_font(size: int):
    for name in [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ]:
        p = Path(name)
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except Exception:
                pass
    return ImageFont.load_default()


def make_poster(path: Path, qr_path: Path) -> None:
    width, height = 1200, 1600
    img = Image.new("RGB", (width, height), "#F5EFE3")
    draw = ImageDraw.Draw(img)

    title_font = load_font(68)
    body_font = load_font(34)
    small_font = load_font(28)

    draw.rounded_rectangle((60, 60, 1140, 1540), radius=36, fill="#FFF9F0", outline="#D9CFBD", width=2)
    draw.text((100, 120), "AI 代做服务工作台", fill="#182126", font=title_font)
    draw.text((100, 230), "自动化脚本 / 资料整理报告 / 轻量 AI workflow", fill="#0E7A6D", font=body_font)

    bullets = [
        "适合“重复但烦、自己做很耗时间”的活",
        "先给一版方案，再决定是否继续扩",
        "可以先看样例、估算价格、再提交需求",
    ]
    y = 340
    for bullet in bullets:
        draw.text((120, y), f"• {bullet}", fill="#5F6A6E", font=body_font)
        y += 70

    qr = Image.open(qr_path).convert("RGB").resize((420, 420))
    img.paste(qr, (390, 760))

    draw.text((320, 1210), "扫码打开中文入口", fill="#182126", font=body_font)
    draw.text((130, 1280), "https://booynal.github.io/ai-service-workbench/zh.html", fill="#5F6A6E", font=small_font)
    draw.text((100, 1380), "先看样例和价格，再决定要不要发需求。", fill="#182126", font=body_font)

    img.save(path)


def main() -> int:
    OUT.mkdir(exist_ok=True)
    qr_path = OUT / "zh-landing-qr.png"
    poster_path = OUT / "wechat-share-card.png"
    make_qr(qr_path)
    make_poster(poster_path, qr_path)
    print(f"Wrote {qr_path}")
    print(f"Wrote {poster_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
