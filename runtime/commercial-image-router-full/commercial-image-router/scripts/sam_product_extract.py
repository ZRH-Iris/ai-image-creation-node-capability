#!/usr/bin/env python3
from pathlib import Path
import argparse
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageDraw
import torch
from segment_anything import sam_model_registry, SamPredictor

RUNTIME_ROOT = Path(__import__('os').environ.get('HERMES_IMAGE_RUNTIME', str(Path.home() / '.hermes-image-runtime')))


def keep_largest_component(mask: np.ndarray) -> np.ndarray:
    num, labels, stats, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), 8)
    if num <= 1:
        return mask.astype(np.uint8)
    areas = stats[1:, cv2.CC_STAT_AREA]
    largest = 1 + int(np.argmax(areas))
    clean = (labels == largest).astype(np.uint8)
    kernel = np.ones((7, 7), np.uint8)
    clean = cv2.morphologyEx(clean, cv2.MORPH_CLOSE, kernel, iterations=2)
    clean = cv2.morphologyEx(clean, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=1)
    return clean


def run(src, outdir, checkpoint, box, points):
    outdir.mkdir(parents=True, exist_ok=True)
    image_bgr = cv2.imread(str(src))
    if image_bgr is None:
        raise SystemExit(f'cannot read {src}')
    image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    h, w = image.shape[:2]

    sam = sam_model_registry['vit_b'](checkpoint=str(checkpoint))
    sam.to('cuda' if torch.cuda.is_available() else 'cpu')
    predictor = SamPredictor(sam)
    predictor.set_image(image)

    # Default prompt: foreground points on the cushion plus background points on
    # the bed/table area. Negative points are important for product cutouts: SAM
    # otherwise tends to include contact shadows or nearby bedding as part of the
    # soft object.
    labels = np.ones(len(points), dtype=np.int32)
    if len(points) >= 6:
        labels[3:] = 0
    masks, scores, _ = predictor.predict(
        point_coords=np.array(points, dtype=np.float32),
        point_labels=labels,
        box=np.array(box, dtype=np.float32),
        multimask_output=True,
    )
    idx = int(np.argmax(scores))
    raw = masks[idx].astype(np.uint8)
    mask = keep_largest_component(raw)

    mask_img = Image.fromarray(mask * 255, 'L')
    # Erode very slightly to remove halo, then feather.
    eroded = cv2.erode(np.array(mask_img), np.ones((3, 3), np.uint8), iterations=1)
    mask_feather = Image.fromarray(eroded, 'L').filter(ImageFilter.GaussianBlur(radius=0.9))
    orig = Image.fromarray(image).convert('RGBA')
    cutout = orig.copy()
    cutout.putalpha(mask_feather)

    bbox = mask_img.getbbox()
    if bbox:
        pad = 8
        bbox = (max(0,bbox[0]-pad), max(0,bbox[1]-pad), min(w,bbox[2]+pad), min(h,bbox[3]+pad))
        cutout_cropped = cutout.crop(bbox)
    else:
        cutout_cropped = cutout

    cutout_path = outdir / 'product_sam_cutout_clean.png'
    cutout_full_path = outdir / 'product_sam_cutout_full_clean.png'
    mask_path = outdir / 'product_sam_mask_clean.png'
    review_path = outdir / 'product_sam_review_clean.png'
    cutout.save(cutout_full_path)
    cutout_cropped.save(cutout_path)
    mask_img.save(mask_path)

    orig_review = Image.fromarray(image).convert('RGB').resize((480, 360))
    d = ImageDraw.Draw(orig_review)
    scale_x, scale_y = 480 / w, 360 / h
    d.rectangle([box[0]*scale_x, box[1]*scale_y, box[2]*scale_x, box[3]*scale_y], outline=(255, 80, 0), width=3)
    mask_review = ImageOps.colorize(mask_img.resize((480, 360)), black=(20,20,20), white=(255,220,0)).convert('RGB')
    checker = Image.new('RGB', (480,360), (235,235,235))
    dc = ImageDraw.Draw(checker)
    for y in range(0,360,24):
        for x in range(0,480,24):
            if (x//24 + y//24) % 2:
                dc.rectangle([x,y,x+23,y+23], fill=(205,205,205))
    preview = Image.alpha_composite(checker.convert('RGBA'), cutout.resize((480,360))).convert('RGB')
    canvas = Image.new('RGB', (1440, 400), (250,250,250))
    canvas.paste(orig_review, (0,40)); canvas.paste(mask_review, (480,40)); canvas.paste(preview, (960,40))
    ImageDraw.Draw(canvas).text((12,10), f'SAM clean mask score={float(scores[idx]):.4f} | largest component + light halo cleanup', fill=(0,0,0))
    canvas.save(review_path)
    print({'cutout': str(cutout_path), 'cutout_full': str(cutout_full_path), 'mask': str(mask_path), 'review': str(review_path), 'score': float(scores[idx]), 'bbox': bbox, 'image_size': (w,h)})


def parse_points(s):
    return [tuple(map(float, pair.split(','))) for pair in s.split(';') if pair]

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default=str(RUNTIME_ROOT / 'image_cache/img_9fefcc18aeb9.jpg'))
    ap.add_argument('--outdir', default=str(RUNTIME_ROOT / 'commercial-image-runtime-tests/product-poster'))
    ap.add_argument('--checkpoint', default=str(RUNTIME_ROOT / 'image-models/sam/sam_vit_b_01ec64.pth'))
    ap.add_argument('--box', default='120,70,1260,1020')
    ap.add_argument('--points', default='720,520;720,320;720,780;1290,890;1170,930;80,930')
    ns = ap.parse_args()
    run(Path(ns.src), Path(ns.outdir), Path(ns.checkpoint), list(map(float, ns.box.split(','))), parse_points(ns.points))
