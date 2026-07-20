# Example Workflows

These are starter API-format workflows for the AI图片制作 runtime. They are ready to run with `scripts/run_workflow.py` once ComfyUI and the listed models are installed.

SD1.5 is intentionally not included in this distribution. The default practical route is JuggernautXL v9 through the SDXL workflow.

| File | Purpose | Required models | Min VRAM |
|------|---------|-----------------|----------|
| `sdxl_txt2img.json` | SDXL/JuggernautXL text-to-image (1024×1024) | `Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors` or another SDXL checkpoint | 8 GB |
| `flux_dev_txt2img.json` | Flux Dev text-to-image (1024×1024) | `flux1-dev.safetensors`, `t5xxl_fp16.safetensors`, `clip_l.safetensors`, `ae.safetensors` | 24 GB (or use fp8 variants) |
| `sdxl_img2img.json` | SDXL/JuggernautXL image-to-image | SDXL-compatible checkpoint | 8 GB |
| `sdxl_inpaint.json` | SDXL/JuggernautXL inpainting (image + mask) | SDXL-compatible checkpoint | 8 GB |
| `upscale_4x.json` | Standalone 4× ESRGAN upscale | `4x-UltraSharp.pth` or another upscaler | 4 GB |
| `wan_video_t2v.json` | Wan 2.x text-to-video (~33 frames) | `wan2.2_t2v_1.3B_fp16.safetensors`, `umt5_xxl_fp16.safetensors`, `wan_2.1_vae.safetensors` | 24 GB |

## Quick start

```bash
# Default image generation route: JuggernautXL through SDXL workflow
python3 ../scripts/run_workflow.py \
  --workflow sdxl_txt2img.json \
  --args '{"ckpt_name":"Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors","prompt":"premium warm lifestyle poster background, commercial photography, no text, no watermark","seed":12345,"steps":20}' \
  --output-dir ./out

# Img2img: upload an input image first via the script's helper
python3 ../scripts/run_workflow.py \
  --workflow sdxl_img2img.json \
  --input-image image=./photo.png \
  --args '{"ckpt_name":"Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors","prompt":"make it watercolor","denoise":0.6}' \
  --output-dir ./out

# What can I tweak in this workflow?
python3 ../scripts/extract_schema.py sdxl_txt2img.json --summary-only

# Are all required models / nodes installed?
python3 ../scripts/check_deps.py sdxl_txt2img.json
```

## Notes

- **Inpaint masks**: white pixels = "regenerate this region", black = preserve. ComfyUI's `LoadImageMask` reads the red channel by default; export your mask as a single-channel image or as normal RGB where red equals mask intensity.
- **Denoise strength** in img2img: `0.0` = output identical to input, `1.0` = ignore input entirely. Sweet spot is usually 0.4–0.7.
- **Flux Dev** needs ~24 GB VRAM in base form. fp8 variants reduce memory.
- **Video workflows** can take many minutes and are not part of the default AI图片制作 install.
- These JSON files are deliberately **API format** (top-level keys are node IDs), not editor format. To open them in ComfyUI's web UI, use `Workflow → Load (API Format)` or `Workflow → Open` and follow the prompt.
- Model names are controllable parameters exposed by `extract_schema.py`; discover installed models from the ComfyUI `/models/...` endpoints or the ComfyUI UI.
