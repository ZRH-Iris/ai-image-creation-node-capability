# Product poster lessons: real mouse photo → commercial poster

Date: 2026-07-19

Context: user supplied a dim real photo of a cream/white wireless mouse on a dark wooden desk and asked for a product promotional image.

## Durable lessons

### 1. Product background generation can violate “no text / no product” prompts

A Qwen-Image-2512 background prompt that asked for a no-text/no-product mouse product stage still generated:

- fake Chinese-looking text in the upper-left area;
- a fake AI-generated mouse on the pedestal.

This failed product-poster QA because it competes with the real user product and introduces hallucinated text. Do not try to hide this with overlay text. Reject the background and either:

1. regenerate a stricter no-text/no-object abstract background; or
2. switch to a deterministic designed background/template when product fidelity matters.

### 2. Keep production-process language out of consumer posters

A draft bottom caption said “真实产品保留 · 科技感场景合成 · 中文模板排版”. This is a workflow/provenance note, not consumer-facing product copy. It should not appear in final promotional images.

For product posters, bottom captions should express buyer-facing value, e.g.:

- “适合办公桌面 · 通勤便携 · 简洁耐看”
- “轻巧机身 · 顺滑滚轮 · 桌面百搭”

Keep process/provenance in the assistant’s report, not on the image.

### 3. If SAM hits GPU OOM, change execution route instead of retrying blindly

When ComfyUI/Qwen occupied GPU 0, SAM segmentation OOMed. The successful route was to run SAM on the other/free GPU:

```bash
CUDA_VISIBLE_DEVICES=1 ${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/comfy-venv/bin/python \
  ${HERMES_HOME:-$HOME/.hermes}/skills/creative/commercial-image-router/scripts/sam_product_extract.py \
  --src /path/to/product.jpg \
  --outdir /path/to/out \
  --box '170,330,1090,900' \
  --points '520,585;750,560;920,620;1200,250;1250,980;80,970'
```

General rule: after one GPU OOM, either use a free GPU, stop the competing ComfyUI job/service, or switch to CPU/lightweight segmentation. Do not run the same failing GPU command again.

### 4. Always inspect the cutout review before poster composition

The successful mouse route visually inspected `product_sam_review_clean.png` before building the poster. Continue only if:

- the product body is complete;
- no large background chunks remain;
- key details such as wheel/buttons/branding are preserved;
- edges are acceptable for the target size.

If the cutout is rough, fix segmentation or use a designed photo-card layout rather than pretending the cutout is clean.
