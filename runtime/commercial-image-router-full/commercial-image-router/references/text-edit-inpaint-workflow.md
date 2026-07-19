# Image Text Edit and Inpaint Workflow

This workflow covers 图片改字 / 擦除旧字 / 局部去物. It is partially verified locally: ComfyUI `sdxl_inpaint.json` runs successfully, but the smoke test showed that basic diffusion inpainting can leave a soft panel/rectangle artifact. Therefore final commercial text edits should combine inpaint with deterministic re-typesetting and visual QA, and may need stronger inpaint tools for complex backgrounds.

## Verified local status

- Dependency check: `${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/comfy-helpers/workflows/sdxl_inpaint.json` is ready.
- Smoke-test source/mask script: `${HERMES_HOME:-$HOME/.hermes}/skills/creative/commercial-image-router/scripts/make_inpaint_smoke_test.py`.
- Smoke-test output: `${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/commercial-image-runtime-tests/inpaint/commercial_inpaint_smoke_00001_.png`.
- Result: old Chinese text was removed, but a soft rounded-rectangle panel remained. This is enough to prove API execution, not enough to call all text-removal tasks commercially solved.

## Recommended route for existing image text replacement

1. **Identify region**
   - Use OCR if available; otherwise visually inspect and define a mask.
   - Mask should cover old text plus its shadow/stroke but not excessive surrounding structure.

2. **Erase old text**
   - Use ComfyUI inpaint or IOPaint/LaMA/BrushNet when installed.
   - For flat posters, do not over-generate; the goal is to restore a clean background or flat panel.

3. **Rebuild text deterministically**
   - Use SVG/Figma/Satori/template layer to render exact replacement text.
   - Match original font family, color, size, alignment, shadow, perspective as much as practical.

4. **QA**
   - Old text is fully gone.
   - New text is exact.
   - No panel scar, blur patch, fake letters, or edge halo.
   - No unrelated drift outside the edit area.

## If the inpaint leaves a visible panel/scar

Do not deliver as final. Choose one:

- Build a deliberate design panel/card over the area so the panel looks intentional.
- Use a stronger inpaint/cleanup tool: IOPaint/LaMA/BrushNet.
- Reconstruct the local background deterministically if it is flat/simple.
- Ask user for layered/source file if the image is a design asset and exact reconstruction matters.

## Command: dependency check

```bash
cd ${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/comfy-helpers
${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/comfy-venv/bin/python scripts/check_deps.py workflows/sdxl_inpaint.json
```

## Command: smoke test

```bash
${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/comfy-venv/bin/python ${HERMES_HOME:-$HOME/.hermes}/skills/creative/commercial-image-router/scripts/make_inpaint_smoke_test.py
cd ${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/comfy-helpers
${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/comfy-venv/bin/python scripts/run_workflow.py \
  --workflow workflows/sdxl_inpaint.json \
  --input-image image=${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/commercial-image-runtime-tests/inpaint/inpaint_test_source.png \
  --input-image mask_image=${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/commercial-image-runtime-tests/inpaint/inpaint_test_mask.png \
  --args '{"ckpt_name":"Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors","prompt":"clean smooth light blue snowy gradient background, no text, no letters, seamless poster background","negative_prompt":"text, letters, words, watermark, logo, ugly, blurry, artifacts, rectangle, sign","steps":18,"cfg":6.0,"sampler_name":"dpmpp_2m","scheduler":"karras","denoise":0.88,"seed":26071901,"filename_prefix":"commercial_inpaint_smoke"}' \
  --output-dir ${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/commercial-image-runtime-tests/inpaint
```

## Upgrade target

Install and verify a stronger dedicated cleanup route:

- IOPaint + LaMA for object/text removal.
- BrushNet or SDXL inpaint model for structure-aware fill.
- AnyText2/ComfyUI_Anytext for cases where text must be integrated into the image texture rather than overlaid.
