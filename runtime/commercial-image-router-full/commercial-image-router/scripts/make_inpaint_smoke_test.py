#!/usr/bin/env python3
from pathlib import Path
import os
from PIL import Image, ImageDraw, ImageFont

runtime_root = Path(os.environ.get('HERMES_IMAGE_RUNTIME', str(Path.home() / '.hermes-image-runtime')))
outdir = runtime_root / 'commercial-image-runtime-tests/inpaint'
outdir.mkdir(parents=True, exist_ok=True)
img = Image.new('RGB', (1024, 1024), (214, 234, 246))
d = ImageDraw.Draw(img)
for y in range(1024):
    c = int(214 + 25 * y / 1024)
    d.line([(0, y), (1024, y)], fill=(190, c, 250))
# fake poster area/text to remove
d.rounded_rectangle([270, 390, 754, 560], radius=26, fill=(255, 255, 255), outline=(40, 90, 130), width=5)
try:
    font = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 62)
except Exception:
    font = ImageFont.load_default()
d.text((332, 440), '需要擦除', fill=(30, 60, 90), font=font)
mask = Image.new('L', (1024, 1024), 0)
md = ImageDraw.Draw(mask)
md.rounded_rectangle([250, 370, 774, 580], radius=34, fill=255)
img.save(outdir/'inpaint_test_source.png')
mask.save(outdir/'inpaint_test_mask.png')
print(outdir/'inpaint_test_source.png')
print(outdir/'inpaint_test_mask.png')
