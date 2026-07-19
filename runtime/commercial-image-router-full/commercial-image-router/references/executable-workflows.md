# Executable Commercial Image Workflows

These are verified local workflows for turning the commercial-image-router from guidance into repeatable execution.

## Product poster: real product + generated scene + SVG typography

Use when the user supplies a product photo and asks for 商品图 / 商品海报 / 宣传图.

### Verified tools

- ComfyUI: `http://127.0.0.1:8188`
- Checkpoint: `Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors`
- Segmentation: SAM ViT-B via `${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/comfy-venv/bin/python`
- Layout/compositing: Node + `sharp` + SVG text template
- Chinese fonts: system `fonts-noto-cjk` package, especially `Noto Sans CJK SC` and `Noto Serif CJK SC`

### Step 1 — Generate empty commercial background

Generate a no-text/no-product background with ComfyUI. Example:

```bash
cd ${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/comfy-helpers
${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/comfy-venv/bin/python scripts/run_workflow.py \
  --workflow workflows/sdxl_txt2img.json \
  --args '{"ckpt_name":"Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors","prompt":"premium ecommerce product photography stage, empty minimalist beige interior corner, travertine stone pedestal platform in foreground, warm plaster wall background, soft side window light, champagne gold and cream color palette, luxury home decor advertising set, clean negative space, no sofa, no bed, no cushion, no pillow, no chair, no product, no text, no logo, no watermark","negative_prompt":"text, letters, watermark, logo, pillow, cushion, sofa, chair, bed, product, clutter, messy, ugly, blurry, low quality, people, packaging","width":1024,"height":1280,"steps":24,"cfg":7.0,"sampler_name":"dpmpp_2m","scheduler":"karras","seed":26071802,"filename_prefix":"pillow_product_pedestal_bg"}' \
  --output-dir ${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/commercial-image-runtime-tests/product-poster
```

QA the generated background before compositing. It must have no text/watermark and no generated version of the user's product that would compete with the real product.

### Step 2 — Extract real product with SAM

```bash
${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/comfy-venv/bin/python \
  ${HERMES_HOME:-$HOME/.hermes}/skills/creative/commercial-image-router/scripts/sam_product_extract.py \
  --src /path/to/product.jpg \
  --outdir ${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/commercial-image-runtime-tests/product-poster
```

The extractor uses foreground points and background points. For a new product photo, inspect the review sheet and adjust `--box` / `--points` instead of accepting a bad cutout.

Outputs:

- `product_sam_cutout_clean.png` — cropped transparent product cutout
- `product_sam_cutout_full_clean.png` — full-frame transparent cutout
- `product_sam_mask_clean.png` — mask
- `product_sam_review_clean.png` — review sheet

### Step 3 — Compose poster with SVG typography

```bash
node ${HERMES_HOME:-$HOME/.hermes}/skills/creative/commercial-image-router/scripts/compose_product_poster.js \
  bg=/path/to/background.png \
  product=/path/to/product_sam_cutout_clean.png \
  out=/path/to/final_product_poster.png \
  title='山水抱枕' \
  subtitle='把东方山水的松弛感，放进客厅' \
  kicker='东方织纹 · 家居软装' \
  caption='暖金山形轮廓 / 细腻山水肌理 / 空间点睛单品'
```

The template renders 1080×1350 PNG, uses Noto CJK font families through SVG, and keeps all Chinese text deterministic.

### Step 4 — QA before delivery

Open/inspect the final PNG. Required checks:

- Chinese text is exact, readable, and not garbled.
- No text overflow: do not place long Chinese selling points or date/location lines as a single SVG `<text>` line inside a fixed box. Split them into separate chips/pills, two-column blocks, or wrapped tspans, then visually inspect every boundary.
- For public-facing camp/admission/event posters, include a deliberate hierarchy: audience badge, large title, emotional subtitle, 2–4 short activity/value chips, then a bottom info panel for time/location/audience. Avoid cramming details into one line.
- Product pixels come from the real user photo, not AI redraw.
- No obvious alpha scraps/white residues from the original background.
- Edges are acceptable; if not, adjust SAM negative points and rerun.
- Product scale and bottom caption do not collide.
- Background has no watermark or accidental text.
- If a generated background contains pseudo-Chinese, random letters, a watermark/logo, or a fake duplicate of the product, reject that background. Do not cover it up; regenerate with a stricter abstract/no-object prompt or switch to a deterministic designed background.
- Final poster copy is buyer-facing, not production-facing. Avoid workflow/provenance text such as “真实产品保留 / 科技感场景合成 / 中文模板排版” inside the image; mention those only in the delivery note if useful.

### Verified sample from this environment

- Background: `${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/commercial-image-runtime-tests/product-poster/pillow_product_pedestal_bg_00001_.png`
- Clean cutout: `${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/commercial-image-runtime-tests/product-poster-neg/product_sam_cutout_clean.png`
- Final poster: `${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/commercial-image-runtime-tests/product-poster/final_product_poster_v5_no_overflow.png`

Visual QA on `final_product_poster_v5_no_overflow.png`: Chinese is clear/no乱码; the earlier text-overflow issue was fixed by splitting long selling points into safe chips; bottom-right white residue from earlier versions is removed; product is the real cushion cutout; background and typography are suitable for user evaluation. Remaining limitation: as a first automated route, edge/shadow fusion can still be improved with dedicated relighting/inpaint passes.

## Important failure rule

If the product cutout review sheet looks bad, do not continue to final poster. Fix segmentation first or choose a design that preserves the original photo in a designed frame. Do not rough-cut and hide the problem with text/layout.
