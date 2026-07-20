#!/usr/bin/env python3
"""Render deterministic Chinese text onto a no-text poster background.

This is a local draft-quality commercial layout layer for Hermes AI图片制作.
It is intentionally deterministic: image models should not render final Chinese.

Example:
  python scripts/render_text_poster.py \
    --background bg.png --output poster.png \
    --title 凝光焕颜 --subtitle 奢宠精华礼盒 \
    --body '晨光凝露质感，点亮肌肤自然光泽' \
    --chips 深层润泽 柔光肤感 礼盒套装 \
    --cta '新品上市 · 限时臻享' --mode luxury
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageStat

FONT_CANDIDATES = {
    "sans": [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.otf",
    ],
    "sans_bold": [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.otf",
    ],
    "serif": [
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSerifCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.otf",
    ],
    "serif_bold": [
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc",
        "/usr/share/fonts/truetype/noto/NotoSerifCJK-Bold.ttc",
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.otf",
    ],
}

MODES = {"luxury", "product", "editorial", "culture", "tech"}


def first_font(kind: str) -> str:
    for f in FONT_CANDIDATES[kind]:
        if Path(f).exists():
            return f
    # last-resort PIL default will not render Chinese well; fail loudly.
    raise SystemExit(f"Missing CJK font for {kind}; install Noto Sans/Serif CJK first")


def luminance(rgb: tuple[int, int, int]) -> float:
    r, g, b = rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def clamp(v: int) -> int:
    return max(0, min(255, v))


def mix(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(clamp(int(a[i] * (1 - t) + b[i] * t)) for i in range(3))


def sample_palette(img: Image.Image) -> dict[str, tuple[int, int, int]]:
    small = img.convert("RGB").resize((64, 96))
    # sample zones where text often lands
    zones = {
        "top": (0, 0, 64, 28),
        "middle": (0, 28, 64, 68),
        "bottom": (0, 68, 64, 96),
    }
    colors = {}
    for name, box in zones.items():
        crop = small.crop(box)
        mean = tuple(int(x) for x in ImageStat.Stat(crop).mean[:3])
        colors[name] = mean
    overall = tuple(int(x) for x in ImageStat.Stat(small).mean[:3])
    colors["overall"] = overall
    # warm accent works for most product/luxury images; still based on palette.
    colors["ink"] = mix((58, 38, 22), colors["overall"], 0.18) if luminance(colors["top"]) > 140 else (248, 242, 226)
    colors["accent"] = mix((190, 145, 72), colors["overall"], 0.25)
    colors["panel"] = mix((255, 248, 232), colors["overall"], 0.18)
    return colors


def text_bbox(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[2] - bb[0], bb[3] - bb[1]


def fit_font(path: str, text: str, max_width: int, start: int, minimum: int = 18) -> ImageFont.FreeTypeFont:
    draw = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    for size in range(start, minimum - 1, -2):
        font = ImageFont.truetype(path, size)
        if text_bbox(draw, text, font)[0] <= max_width:
            return font
    return ImageFont.truetype(path, minimum)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    if not text:
        return []
    lines: list[str] = []
    current = ""
    for ch in text:
        test = current + ch
        if text_bbox(draw, test, font)[0] <= max_width or not current:
            current = test
        else:
            lines.append(current)
            current = ch
    if current:
        lines.append(current)
    return lines


def add_gradient_veil(img: Image.Image, mode: str) -> Image.Image:
    w, h = img.size
    veil = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(veil)
    if mode in {"luxury", "product", "culture"}:
        top_color = (255, 248, 232)
        bottom_color = (70, 45, 24)
    elif mode == "tech":
        top_color = (235, 244, 255)
        bottom_color = (9, 18, 32)
    else:
        top_color = (255, 255, 255)
        bottom_color = (18, 18, 18)
    for y in range(0, int(h * 0.42)):
        t = 1 - y / (h * 0.42)
        alpha = int(112 * (t**1.6))
        d.line([(0, y), (w, y)], fill=(*top_color, alpha))
    for y in range(int(h * 0.72), h):
        t = (y - int(h * 0.72)) / (h * 0.28)
        alpha = int(70 * (t**1.35))
        d.line([(0, y), (w, y)], fill=(*bottom_color, alpha))
    return Image.alpha_composite(img, veil)


def draw_soft_text(layer: Image.Image, pos: tuple[float, float], text: str, font: ImageFont.FreeTypeFont,
                   fill: tuple[int, int, int, int], anchor: str = "mm", stroke: tuple[int, tuple[int, int, int, int]] | None = None) -> None:
    x, y = pos
    shadow = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    stroke_width, stroke_fill = stroke or (0, (0, 0, 0, 0))
    sd.text((x + 3, y + 5), text, font=font, fill=(65, 42, 22, 72), anchor=anchor,
            stroke_width=stroke_width, stroke_fill=(255, 250, 235, 28))
    shadow = shadow.filter(ImageFilter.GaussianBlur(3.2))
    layer.alpha_composite(shadow)
    d = ImageDraw.Draw(layer)
    d.text((x, y), text, font=font, fill=fill, anchor=anchor,
           stroke_width=stroke_width, stroke_fill=stroke_fill)


def render(args: argparse.Namespace) -> None:
    bg = Image.open(args.background).convert("RGBA")
    w, h = bg.size
    palette = sample_palette(bg)
    base = add_gradient_veil(bg, args.mode)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    serif = first_font("serif_bold" if args.mode in {"luxury", "culture"} else "sans_bold")
    sans = first_font("sans")
    sans_bold = first_font("sans_bold")

    ink = (*palette["ink"], 255)
    accent = (*palette["accent"], 235)
    panel = (*palette["panel"], 154)
    light_text = (255, 248, 232, 238)

    # Brand/kicker
    if args.kicker:
        k_font = fit_font(sans_bold, args.kicker, int(w * 0.78), max(22, int(h * 0.022)), 18)
        draw.text((w / 2, h * 0.055), args.kicker, font=k_font, fill=accent, anchor="mm")
        line_w = int(w * 0.28)
        draw.rounded_rectangle((w / 2 - line_w / 2, h * 0.082, w / 2 + line_w / 2, h * 0.084), radius=2, fill=accent)

    # Title and subtitle
    title_font = fit_font(serif, args.title, int(w * 0.80), int(h * 0.062), int(h * 0.038))
    draw_soft_text(layer, (w / 2, h * 0.125), args.title, title_font, ink, stroke=(1, (255, 250, 235, 88)))

    if args.subtitle:
        subtitle_font = fit_font(serif, args.subtitle, int(w * 0.80), int(h * 0.040), int(h * 0.028))
        draw_soft_text(layer, (w / 2, h * 0.185), args.subtitle, subtitle_font, (*mix(palette["ink"], palette["accent"], 0.28), 250), stroke=(1, (255, 250, 235, 70)))

    if args.body:
        body_font = fit_font(sans, args.body, int(w * 0.78), int(h * 0.023), 18)
        lines = wrap_text(draw, args.body, body_font, int(w * 0.78))[:2]
        y = h * 0.240
        for line in lines:
            draw.text((w / 2, y), line, font=body_font, fill=(*mix(palette["ink"], palette["overall"], 0.18), 232), anchor="mm")
            y += body_font.size * 1.35

    # CTA/badge
    if args.cta:
        cta_font = fit_font(sans_bold, args.cta, int(w * 0.62), int(h * 0.024), 18)
        tw, th = text_bbox(draw, args.cta, cta_font)
        px, py = int(w * 0.035), int(h * 0.012)
        by = int(h * 0.300)
        bx1, bx2 = int(w / 2 - tw / 2 - px), int(w / 2 + tw / 2 + px)
        draw.rounded_rectangle((bx1, by, bx2, by + th + py * 2), radius=int(h * 0.020), fill=panel, outline=(*palette["accent"], 145), width=2)
        draw.text((w / 2, by + th / 2 + py - 1), args.cta, font=cta_font, fill=(*mix(palette["ink"], palette["accent"], 0.20), 245), anchor="mm")

    # Bottom chips
    chips = [c for c in args.chips if c.strip()]
    if chips:
        chip_font = ImageFont.truetype(sans_bold, max(22, int(h * 0.023)))
        gap = int(w * 0.020)
        sizes = []
        for chip in chips:
            cw, ch = text_bbox(draw, chip, chip_font)
            sizes.append((cw + int(w * 0.045), ch + int(h * 0.018)))
        total = sum(x for x, _ in sizes) + gap * (len(sizes) - 1)
        x = int(w / 2 - total / 2)
        y = int(h * 0.365)
        for chip, (cw, ch) in zip(chips, sizes):
            draw.rounded_rectangle((x, y, x + cw, y + ch), radius=ch // 2, fill=(*palette["panel"], 172), outline=(*palette["accent"], 132), width=1)
            draw.text((x + cw / 2, y + ch / 2 - 1), chip, font=chip_font, fill=(*palette["ink"], 242), anchor="mm")
            x += cw + gap

    if args.footer:
        f_font = fit_font(sans, args.footer, int(w * 0.82), int(h * 0.022), 18)
        draw.text((w / 2, h * 0.948), args.footer, font=f_font, fill=light_text, anchor="mm")

    final = Image.alpha_composite(base, layer).convert("RGB")
    final.save(args.output, quality=96)


def main(argv: Iterable[str] | None = None) -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--background", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--subtitle", default="")
    p.add_argument("--body", default="")
    p.add_argument("--kicker", default="")
    p.add_argument("--cta", default="")
    p.add_argument("--footer", default="")
    p.add_argument("--chips", nargs="*", default=[])
    p.add_argument("--mode", choices=sorted(MODES), default="product")
    args = p.parse_args(argv)
    render(args)


if __name__ == "__main__":
    main()
