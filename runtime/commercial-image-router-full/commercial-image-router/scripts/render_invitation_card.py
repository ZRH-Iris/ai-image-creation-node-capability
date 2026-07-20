#!/usr/bin/env python3
"""Render deterministic Chinese invitation text onto a blank-card background.

Use after generating a decorated no-text background with a clean blank card area.
Do not use image models to render final Chinese event facts.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT_CANDIDATES = {
    "serif": [
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSerifCJK-Regular.ttc",
    ],
    "serif_bold": [
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc",
        "/usr/share/fonts/truetype/noto/NotoSerifCJK-Bold.ttc",
    ],
    "sans": [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    ],
    "sans_bold": [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
    ],
}


def first_font(kind: str) -> str:
    for f in FONT_CANDIDATES[kind]:
        if Path(f).exists():
            return f
    raise SystemExit(f"Missing CJK font for {kind}; install Noto CJK first")


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def bbox(draw: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont) -> tuple[int, int]:
    b = draw.textbbox((0, 0), text, font=f)
    return b[2] - b[0], b[3] - b[1]


def fit(draw: ImageDraw.ImageDraw, path: str, text: str, max_w: int, start: int, minimum: int = 20) -> ImageFont.FreeTypeFont:
    for s in range(start, minimum - 1, -2):
        f = font(path, s)
        if bbox(draw, text, f)[0] <= max_w:
            return f
    return font(path, minimum)


def soft_text(layer: Image.Image, pos: tuple[float, float], text: str, f: ImageFont.FreeTypeFont,
              fill: tuple[int, int, int, int], anchor: str = "mm", stroke: int = 0,
              stroke_fill: tuple[int, int, int, int] = (255, 248, 236, 120), shadow: bool = True) -> None:
    x, y = pos
    if shadow:
        sh = Image.new("RGBA", layer.size, (0, 0, 0, 0))
        sd = ImageDraw.Draw(sh)
        sd.text((x + 2, y + 4), text, font=f, anchor=anchor, fill=(116, 70, 38, 58),
                stroke_width=stroke, stroke_fill=(255, 248, 238, 20))
        sh = sh.filter(ImageFilter.GaussianBlur(2.8))
        layer.alpha_composite(sh)
    d = ImageDraw.Draw(layer)
    d.text((x, y), text, font=f, anchor=anchor, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)


def draw_info_row(draw: ImageDraw.ImageDraw, x_center: float, y: int, width: int, height: int,
                  label: str, value: str, label_font: ImageFont.FreeTypeFont, value_font: ImageFont.FreeTypeFont,
                  palette: dict[str, tuple[int, int, int, int]]) -> None:
    x1, x2 = int(x_center - width / 2), int(x_center + width / 2)
    draw.rounded_rectangle((x1, y, x2, y + height), radius=height // 2,
                           fill=palette["row_fill"], outline=palette["line"], width=2)
    draw.text((x1 + width * 0.18, y + height / 2 - 1), label, font=label_font,
              fill=palette["label"], anchor="mm")
    sep_x = x1 + width * 0.29
    draw.rounded_rectangle((sep_x, y + height * 0.24, sep_x + 2, y + height * 0.76), radius=1,
                           fill=palette["line_soft"])
    draw.text((x1 + width * 0.63, y + height / 2 - 2), value, font=value_font,
              fill=palette["main"], anchor="mm")


def render(args: argparse.Namespace) -> None:
    bg = Image.open(args.background).convert("RGBA")
    w, h = bg.size
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    serif = first_font("serif")
    serif_bold = first_font("serif_bold")
    sans = first_font("sans")
    sans_bold = first_font("sans_bold")

    cx = w / 2
    card_margin_x = int(w * 0.205)
    max_text_w = w - card_margin_x * 2 - int(w * 0.055)

    palette = {
        "main": (110, 70, 39, 255),
        "title": (126, 78, 41, 255),
        "sub": (157, 100, 55, 238),
        "gold": (178, 125, 67, 230),
        "line": (218, 172, 94, 170),
        "line_soft": (218, 172, 94, 130),
        "row_fill": (255, 244, 229, 178),
        "label": (176, 121, 62, 245),
    }

    # Gentle veil inside the card area for readability. Assumes centered blank card.
    veil = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    vd = ImageDraw.Draw(veil)
    vd.rounded_rectangle((int(w * 0.20), int(h * 0.15), int(w * 0.80), int(h * 0.81)),
                         radius=int(w * 0.055), fill=(255, 252, 244, 52))
    layer.alpha_composite(veil)

    kicker_f = font(sans, max(24, int(h * 0.022)))
    soft_text(layer, (cx, h * 0.202), args.kicker, kicker_f, palette["gold"], shadow=False)
    draw = ImageDraw.Draw(layer)
    line_w = int(w * 0.23)
    draw.rounded_rectangle((cx - line_w / 2, h * 0.228, cx + line_w / 2, h * 0.231),
                           radius=2, fill=(213, 168, 92, 160))

    title_f = fit(draw, serif_bold, args.event, max_text_w, int(h * 0.060), int(h * 0.038))
    soft_text(layer, (cx, h * 0.292), args.event, title_f, palette["title"], stroke=1, shadow=True)

    if args.subtitle:
        sub_f = fit(draw, sans, args.subtitle, max_text_w, int(h * 0.028), int(h * 0.020))
        soft_text(layer, (cx, h * 0.352), args.subtitle, sub_f, palette["sub"], shadow=False)

    blessing_f = font(serif, max(26, int(h * 0.025)))
    y = h * 0.428
    for line in args.blessing[:5]:
        soft_text(layer, (cx, y), line, blessing_f, (138, 88, 50, 242), shadow=False)
        y += blessing_f.size * 1.45

    row_label_f = font(sans, max(22, int(h * 0.018)))
    row_value_f = fit(draw, sans_bold, max(args.date, args.venue, key=len), int(w * 0.48), max(28, int(h * 0.024)), 22)
    row_w = int(w * 0.51)
    row_h = int(h * 0.051)
    row_y = int(h * 0.610)
    draw = ImageDraw.Draw(layer)
    draw_info_row(draw, cx, row_y, row_w, row_h, args.date_label, args.date, row_label_f, row_value_f, palette)
    draw_info_row(draw, cx, row_y + int(row_h * 1.33), row_w, row_h, args.venue_label, args.venue, row_label_f, row_value_f, palette)

    if args.closing:
        close_f = fit(draw, sans, args.closing, max_text_w, max(22, int(h * 0.020)), 18)
        soft_text(layer, (cx, h * 0.735), args.closing, close_f, (151, 96, 54, 235), shadow=False)
    if args.footer:
        footer_f = fit(draw, sans, args.footer, max_text_w, max(21, int(h * 0.019)), 18)
        soft_text(layer, (cx, h * 0.767), args.footer, footer_f, (151, 96, 54, 218), shadow=False)

    # Small flourish.
    draw = ImageDraw.Draw(layer)
    fy = h * 0.795
    draw.arc((cx - 70, fy - 20, cx - 20, fy + 24), start=210, end=330, fill=(210, 160, 87, 150), width=2)
    draw.arc((cx + 20, fy - 20, cx + 70, fy + 24), start=210, end=330, fill=(210, 160, 87, 150), width=2)
    draw.ellipse((cx - 8, fy, cx + 8, fy + 16), fill=(218, 172, 94, 150))

    final = Image.alpha_composite(bg, layer).convert("RGB")
    final.save(args.output, quality=96)


def main(argv: Iterable[str] | None = None) -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--background", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--event", required=True)
    p.add_argument("--subtitle", default="")
    p.add_argument("--date", required=True)
    p.add_argument("--venue", required=True)
    p.add_argument("--blessing", nargs="+", default=[])
    p.add_argument("--kicker", default="诚 邀 莅 临")
    p.add_argument("--date-label", default="时间")
    p.add_argument("--venue-label", default="地点")
    p.add_argument("--closing", default="诚盼您携温暖祝福莅临见证")
    p.add_argument("--footer", default="让爱与喜悦，陪伴这个珍贵时刻")
    args = p.parse_args(argv)
    if not args.blessing:
        args.blessing = ["愿美好与喜悦相伴", "诚邀您共同见证"]
    render(args)


if __name__ == "__main__":
    main()
