# Upscale and Repair Workflow

Use this route when the user asks for 高清、放大、修复、提清晰度、适配印刷/大图交付, or when a generated public-facing image is good but needs a higher-resolution deliverable.

## Verified local status

- ComfyUI upscale workflow is dependency-ready: `${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/comfy-helpers/workflows/upscale_4x.json`.
- Model installed: `${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/comfy-workspace/models/upscale_models/4x-UltraSharp.pth`.
- Model size: `66961958` bytes.
- Model sha256: `a5812231fc936b42af08a5edba784195495d303d5b3248c24489ef0c4021fe01`.
- Smoke test input: `${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/examples/changbaishan_winter_camp_poster_v1.png` at `1080×1350`.
- Verified output: `${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/commercial-image-runtime-tests/upscale/winter_poster_4x_ultrasharp_00001_.png` at `4320×5400`.
- Visual QA: Chinese text remained readable and accurate; no obvious watermark or text distortion; this route is verified for high-resolution poster upscaling.

## When to use

Use for:

- User asks for higher resolution or print-ready output.
- A poster/social image is approved at 1080–1350px scale and needs a large version.
- A generated illustration is good but slightly soft.
- Delivery requires both preview and high-resolution files.

Do **not** use blindly for:

- Images with already-bad text layout or typo — fix layout first, upscale last.
- Product photos where package text/logo fidelity is critical and the upscaler distorts small text; QA against original.
- Faces where the face is already distorted; use face-specific repair only when appropriate and inspect identity drift.

## Command

```bash
cd ${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/comfy-helpers
${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/comfy-venv/bin/python scripts/run_workflow.py \
  --workflow workflows/upscale_4x.json \
  --input-image image=/path/to/input.png \
  --args '{"upscale_model_name":"4x-UltraSharp.pth","filename_prefix":"my_image_4x_ultrasharp"}' \
  --output-dir /path/to/output-dir
```

## QA checklist

- Input was already approved at normal size.
- Output dimensions are correct, usually 4× width and 4× height.
- Chinese text remains exact and readable.
- No ringing halos around title text or product edges.
- Product logos/labels are not warped.
- Faces do not become plastic or change identity.
- File opens correctly and is delivered as an attachment when final.

## Practical delivery rule

For public-facing images, keep both:

- Normal share size, e.g. `1080×1350` for mobile/social.
- High-res version, e.g. `4320×5400`, when the user asks for高清/印刷/大图.

Do not replace the normal social image with a huge file unless the user asks; some platforms compress large images aggressively.
