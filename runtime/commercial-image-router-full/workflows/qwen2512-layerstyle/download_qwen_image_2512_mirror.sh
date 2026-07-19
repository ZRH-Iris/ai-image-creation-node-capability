#!/usr/bin/env bash
set -euo pipefail
BASE=${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/comfy-workspace/models
MIRROR=https://hf-mirror.com
mkdir -p "$BASE/diffusion_models" "$BASE/text_encoders" "$BASE/vae" "$BASE/loras"

download() {
  local path="$1" out="$2"
  local url="$MIRROR/$path"
  mkdir -p "$(dirname "$out")"
  if [ -s "$out" ]; then
    echo "[skip] exists $out ($(du -h "$out" | cut -f1))"
    return 0
  fi
  echo "[download] $url -> $out"
  tmp="$out.part"
  curl -L --fail --retry 20 --retry-delay 5 --retry-all-errors -C - --speed-time 60 --speed-limit 1024 -o "$tmp" "$url"
  mv "$tmp" "$out"
  echo "[done] $out ($(du -h "$out" | cut -f1))"
}

download "Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors" "$BASE/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors"
download "Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/vae/qwen_image_vae.safetensors" "$BASE/vae/qwen_image_vae.safetensors"
download "Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/diffusion_models/qwen_image_2512_fp8_e4m3fn.safetensors" "$BASE/diffusion_models/qwen_image_2512_fp8_e4m3fn.safetensors"
download "lightx2v/Qwen-Image-2512-Lightning/resolve/main/Qwen-Image-2512-Lightning-4steps-V1.0-fp32.safetensors" "$BASE/loras/Qwen-Image-2512-Lightning-4steps-V1.0-fp32.safetensors"

echo "qwen_image_2512_mirror_download_complete"
