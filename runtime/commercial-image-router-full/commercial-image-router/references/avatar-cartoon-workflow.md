# Avatar / Cartoon Portrait Workflow

Use when the user supplies a real-person photo and asks for 动漫头像 / 卡通头像 / 微信头像.

## Intake and safety

- Do not identify the person. Describe only visible traits useful for generation: glasses, hair, face shape, expression, clothing, pose, background, and crop.
- Preserve the user's visible identity cues, but generate a stylized avatar, not a biometric identification result.
- For this user, favor a clearly cartoon/anime result that still resembles the reference: round glasses, natural black hair, gentle expression, and enough breathing room for WeChat circular crop.

## Practical local workflow

### 1. Prepare a square reference image

Make a 1024×1024 source with the face centered and breathing room. Avoid tight crops; WeChat will circular-crop the final image.

Recommended approach:

- Use the original photo as the central layer.
- Add a blurred/softened version of the photo as the square background if the source is portrait-shaped.
- Keep head/shoulders visible and leave margins around hair and shoulders.

### 2. Run ComfyUI img2img

Use `workflows/sdxl_img2img.json` through the ComfyUI skill. Current working route:

```bash
cd ${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/comfy-helpers
${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/comfy-venv/bin/python scripts/run_workflow.py \
  --workflow workflows/sdxl_img2img.json \
  --input-image image=/path/to/avatar_source_square.png \
  --args '{"ckpt_name":"Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors","prompt":"obvious anime cartoon WeChat avatar based on reference face, not photorealistic, clean 2D illustration, young woman with round silver rim glasses, straight black shoulder length hair, soft bangs, gentle warm smile, cute natural Chinese girl character, large expressive eyes but still similar, cream knit top, soft pastel scenic background, centered head and shoulders, enough empty margin for circular crop, polished avatar icon, no text, no watermark","negative_prompt":"photorealistic, realistic skin pores, text, watermark, logo, low quality, blurry, distorted face, extra eyes, bad eyes, deformed glasses, crooked glasses, extra fingers, bad hands, old, masculine, heavy makeup, cropped head, out of frame","steps":30,"cfg":8.0,"sampler_name":"dpmpp_2m","scheduler":"karras","denoise":0.68,"seed":412001,"filename_prefix":"wechat_anime_avatar_cartoon"}' \
  --output-dir /path/to/output
```

### 3. Generate at least two stylization strengths

Do not stop at the first img2img output. Run at least:

- `denoise` around `0.50–0.55` for stronger likeness but often too photorealistic.
- `denoise` around `0.65–0.72` for clearer anime/cartoon style.

Choose the version that best balances similarity and cartoon style. If the user explicitly asks for “动漫风/卡通一点”, do not deliver a near-photorealistic beauty-filter result unless no better candidate exists.

## QA checklist

- Round glasses are intact and not warped.
- Hair length/color and bangs remain close to the reference.
- Expression and overall temperament remain similar.
- Style is visibly anime/cartoon, not merely beautified photo.
- Face is centered with margins for circular crop.
- No text, watermark, extra eyes, distorted glasses, or strange hands.
- If the source photo includes distracting background, the avatar output should simplify or replace it with a soft scenic/background layer.

## Delivery

Send the selected final PNG directly as `MEDIA:/absolute/path`. If multiple candidates are useful, send the best one first and mention that more variants can be generated.