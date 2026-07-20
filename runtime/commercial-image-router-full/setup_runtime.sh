#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
RUNTIME="${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}"
COMFY="$RUNTIME/comfy-workspace"
VENV="$RUNTIME/comfy-venv"
HELPERS="$RUNTIME/comfy-helpers"
LAYOUT="$RUNTIME/image-layout"
HF_BASE="${HF_ENDPOINT:-https://huggingface.co}"
PROFILE="core-generate"
RUN_SMOKE=1
DRY_RUN=0
INSTALL_LAYOUT=0
INSTALL_COMFY_STACK=1
INSTALL_JUGGERNAUT=1
INSTALL_QWEN=0
INSTALL_SDXL_BASE=0
INSTALL_SKILL_ONLY=0

usage(){
  cat <<'EOF'
AI图片制作 runtime installer

默认安装：--profile core-generate
  安装 commercial-image-router Skill + ComfyUI + PyTorch + JuggernautXL + 基础 txt2img workflow，并运行 smoke test。

Profiles:
  --profile skill-only      只安装 Skill/规则，不装 ComfyUI/模型。
  --profile core-generate  默认。装 ComfyUI/PyTorch/JuggernautXL/基础 txt2img workflow。
  --profile layout         只加装 Node/SVG 中文排版层。
  --profile qwen           装 ComfyUI/PyTorch/Qwen-Image-2512 workflow 和模型（约30GB+）。
  --profile creator        装 core-generate + layout + Qwen。
  --profile sdxl-base      在当前 ComfyUI 环境中加装 SDXL Base 兼容模型。
  --profile full           装 creator + SDXL Base。商品图/SAM/放大修复后续按需扩展，不默认塞入。

Other flags:
  --dry-run                不下载大文件，模拟目录、Skill、smoke artifact。
  --no-smoke-test          跳过 smoke test。
  --skip-model-download    只装环境和 workflow，不下载模型。
  --install-skill-only     兼容旧参数，等同 --profile skill-only。
EOF
}

for arg in "$@"; do
  case "$arg" in
    --help|-h) usage; exit 0 ;;
    --profile=*) PROFILE="${arg#*=}" ;;
    --profile) echo "Use --profile=name" >&2; exit 2 ;;
    --no-smoke-test) RUN_SMOKE=0 ;;
    --dry-run) DRY_RUN=1 ;;
    --skip-model-download) INSTALL_JUGGERNAUT=0; INSTALL_QWEN=0; INSTALL_SDXL_BASE=0 ;;
    --install-skill-only) PROFILE="skill-only" ;;
    *) echo "Unknown option: $arg" >&2; usage >&2; exit 2 ;;
  esac
done

case "$PROFILE" in
  skill-only)
    INSTALL_SKILL_ONLY=1; INSTALL_COMFY_STACK=0; INSTALL_JUGGERNAUT=0; INSTALL_QWEN=0; INSTALL_SDXL_BASE=0; INSTALL_LAYOUT=0; RUN_SMOKE=0 ;;
  core-generate)
    INSTALL_COMFY_STACK=1; INSTALL_JUGGERNAUT=1; INSTALL_QWEN=0; INSTALL_SDXL_BASE=0; INSTALL_LAYOUT=0 ;;
  layout)
    INSTALL_COMFY_STACK=0; INSTALL_JUGGERNAUT=0; INSTALL_QWEN=0; INSTALL_SDXL_BASE=0; INSTALL_LAYOUT=1; RUN_SMOKE=0 ;;
  qwen)
    INSTALL_COMFY_STACK=1; INSTALL_JUGGERNAUT=0; INSTALL_QWEN=1; INSTALL_SDXL_BASE=0; INSTALL_LAYOUT=0 ;;
  creator)
    INSTALL_COMFY_STACK=1; INSTALL_JUGGERNAUT=1; INSTALL_QWEN=1; INSTALL_SDXL_BASE=0; INSTALL_LAYOUT=1 ;;
  sdxl-base)
    INSTALL_COMFY_STACK=1; INSTALL_JUGGERNAUT=0; INSTALL_QWEN=0; INSTALL_SDXL_BASE=1; INSTALL_LAYOUT=0 ;;
  full)
    INSTALL_COMFY_STACK=1; INSTALL_JUGGERNAUT=1; INSTALL_QWEN=1; INSTALL_SDXL_BASE=1; INSTALL_LAYOUT=1 ;;
  *) echo "Unknown profile: $PROFILE" >&2; usage >&2; exit 2 ;;
esac

log(){ printf '\033[32m[ai-image-runtime]\033[0m %s\n' "$*"; }
warn(){ printf '\033[33m[warn]\033[0m %s\n' "$*"; }
fail(){ printf '\033[31m[error]\033[0m %s\n' "$*" >&2; exit 1; }
need_cmd(){ command -v "$1" >/dev/null 2>&1 || fail "Missing command: $1"; }

install_skill(){
  log "Installing Skill into $HERMES_HOME/skills/creative/commercial-image-router"
  mkdir -p "$HERMES_HOME/skills/creative"
  rm -rf "$HERMES_HOME/skills/creative/commercial-image-router"
  cp -a "$ROOT_DIR/commercial-image-router" "$HERMES_HOME/skills/creative/"
}

install_system_deps(){
  log "Checking system dependencies"
  if [ "$DRY_RUN" = "1" ]; then
    warn "[dry-run] skipping apt installs and command checks"
    return
  fi
  if command -v apt-get >/dev/null 2>&1; then
    if [ "$(id -u)" = "0" ]; then SUDO=""; else SUDO="sudo"; fi
    if command -v sudo >/dev/null 2>&1 || [ "$(id -u)" = "0" ]; then
      $SUDO apt-get update -qq || true
      $SUDO apt-get install -y -qq git curl ca-certificates fonts-noto-cjk fonts-noto-cjk-extra || true
      if [ "$INSTALL_LAYOUT" = "1" ]; then
        $SUDO apt-get install -y -qq nodejs npm || true
      fi
      fc-cache -f || true
    else
      warn "apt found but sudo unavailable; install git/curl and optional node/npm/fonts manually if missing."
    fi
  else
    warn "Non-apt system: install git, curl, and Noto CJK fonts manually if missing."
  fi
  need_cmd git
  need_cmd curl
  if [ "$INSTALL_LAYOUT" = "1" ]; then need_cmd node; need_cmd npm; fi
}

install_uv(){
  if [ "$DRY_RUN" = "1" ]; then
    mkdir -p "$VENV"
    warn "[dry-run] created placeholder venv directory at $VENV"
    return
  fi
  if command -v uv >/dev/null 2>&1; then return; fi
  log "Installing uv"
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
  command -v uv >/dev/null 2>&1 || fail "uv install failed; install uv manually."
}

install_comfy(){
  mkdir -p "$RUNTIME"
  if [ "$DRY_RUN" = "1" ]; then
    mkdir -p "$COMFY" "$VENV" "$COMFY/models/checkpoints" "$COMFY/models/diffusion_models" "$COMFY/models/text_encoders" "$COMFY/models/vae" "$COMFY/models/loras"
    warn "[dry-run] prepared placeholder ComfyUI directories"
    return
  fi
  if [ ! -d "$COMFY/.git" ]; then
    log "Cloning ComfyUI into $COMFY"
    git clone --depth 1 https://github.com/comfyanonymous/ComfyUI.git "$COMFY"
  else
    log "ComfyUI already exists; pulling latest"
    git -C "$COMFY" pull --ff-only || warn "ComfyUI pull failed; continuing with existing checkout."
  fi
  log "Creating Python venv at $VENV"
  uv venv --clear --python 3.12 "$VENV" || uv venv --clear "$VENV"
  log "Installing PyTorch for local model inference"
  uv pip install --python "$VENV/bin/python" torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu130 \
    || uv pip install --python "$VENV/bin/python" torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128 \
    || uv pip install --python "$VENV/bin/python" torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 \
    || uv pip install --python "$VENV/bin/python" torch torchvision torchaudio
  log "Installing ComfyUI requirements"
  uv pip install --python "$VENV/bin/python" -r "$COMFY/requirements.txt"
}

install_helpers(){
  log "Installing ComfyUI helper workflows/scripts into $HELPERS"
  mkdir -p "$HELPERS"
  rm -rf "$HELPERS/scripts" "$HELPERS/workflows"
  cp -a "$ROOT_DIR/comfy-helpers/scripts" "$HELPERS/scripts"
  cp -a "$ROOT_DIR/comfy-helpers/workflows" "$HELPERS/workflows"
  chmod +x "$HELPERS/scripts"/*.py || true
}

install_layout(){
  if [ "$INSTALL_LAYOUT" != "1" ]; then
    return 0
  fi
  log "Installing optional Node/SVG layout runtime into $LAYOUT"
  mkdir -p "$LAYOUT"
  if [ "$DRY_RUN" = "1" ]; then
    warn "[dry-run] skipping npm layout installs; directory created at $LAYOUT"
    return
  fi
  if [ ! -f "$LAYOUT/package.json" ]; then
    (cd "$LAYOUT" && npm init -y >/dev/null)
  fi
  (cd "$LAYOUT" && npm install sharp @resvg/resvg-js)
}

url_for(){
  local url="$1"
  if [ "$HF_BASE" != "https://huggingface.co" ]; then
    url="${url/https:\/\/huggingface.co/$HF_BASE}"
  fi
  printf '%s' "$url"
}

download_file(){
  local name="$1" rel="$2" url="$3" sha="${4:-}"
  local dest="$RUNTIME/$rel"
  if [ "$DRY_RUN" = "1" ]; then
    mkdir -p "$(dirname "$dest")"
    warn "[dry-run] would download $name to $dest"
    return
  fi
  mkdir -p "$(dirname "$dest")"
  if [ -s "$dest" ]; then
    if [ -n "$sha" ]; then
      local got
      got="$(sha256sum "$dest" | awk '{print $1}')"
      if [ "$got" = "$sha" ]; then log "$name already present and sha256 ok"; return; fi
      warn "$name exists but sha mismatch; re-downloading"
    else
      log "$name already present"
      return
    fi
  fi
  local final_url
  final_url="$(url_for "$url")"
  log "Downloading $name"
  log "$final_url"
  curl -L --fail --retry 8 --retry-delay 5 --continue-at - -o "$dest" "$final_url"
  if [ -n "$sha" ]; then echo "$sha  $dest" | sha256sum -c -; fi
}

install_models(){
  if [ "$INSTALL_JUGGERNAUT" = "1" ]; then
    download_file "JuggernautXL v9 primary model" "comfy-workspace/models/checkpoints/Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors" \
      "https://huggingface.co/RunDiffusion/Juggernaut-XL-v9/resolve/main/Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors?download=true" \
      "c9e3e68f89b8e38689e1097d4be4573cf308de4e3fd044c64ca697bdb4aa8bca"
  fi
  if [ "$INSTALL_SDXL_BASE" = "1" ]; then
    download_file "SDXL base compatibility fallback" "comfy-workspace/models/checkpoints/sd_xl_base_1.0.safetensors" \
      "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors?download=true" ""
  fi
  if [ "$INSTALL_QWEN" = "1" ]; then
    download_file "Qwen text encoder" "comfy-workspace/models/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors" \
      "https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors" ""
    download_file "Qwen VAE" "comfy-workspace/models/vae/qwen_image_vae.safetensors" \
      "https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/vae/qwen_image_vae.safetensors" ""
    download_file "Qwen Image 2512 fp8" "comfy-workspace/models/diffusion_models/qwen_image_2512_fp8_e4m3fn.safetensors" \
      "https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/diffusion_models/qwen_image_2512_fp8_e4m3fn.safetensors" ""
    download_file "Qwen Image 2512 Lightning LoRA" "comfy-workspace/models/loras/Qwen-Image-2512-Lightning-4steps-V1.0-fp32.safetensors" \
      "https://huggingface.co/lightx2v/Qwen-Image-2512-Lightning/resolve/main/Qwen-Image-2512-Lightning-4steps-V1.0-fp32.safetensors" ""
  fi
}

write_launcher(){
  log "Writing launcher scripts"
  mkdir -p "$RUNTIME"
  cat > "$RUNTIME/start_comfy.sh" <<EOF
#!/usr/bin/env bash
set -euo pipefail
cd "$COMFY"
exec "$VENV/bin/python" main.py --listen 127.0.0.1 --port 8188
EOF
  chmod +x "$RUNTIME/start_comfy.sh"
  cat > "$RUNTIME/run_smoke_test.sh" <<EOF
#!/usr/bin/env bash
set -euo pipefail
export HERMES_IMAGE_RUNTIME="$RUNTIME"
cd "$HELPERS"
"$VENV/bin/python" scripts/run_workflow.py \
  --workflow workflows/sdxl_txt2img.json \
  --args '{"ckpt_name":"Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors","prompt":"premium warm lifestyle poster background, commercial photography, clean composition, no text, no watermark","negative_prompt":"text, letters, watermark, logo, blurry, deformed, low quality","width":768,"height":960,"steps":12,"cfg":6,"sampler_name":"dpmpp_2m","scheduler":"karras","seed":20260720,"filename_prefix":"ai_image_creation_core_smoke"}' \
  --output-dir "$RUNTIME/smoke-test-output"
EOF
  chmod +x "$RUNTIME/run_smoke_test.sh"
}

run_smoke(){
  if [ "$RUN_SMOKE" = "0" ]; then return; fi
  if [ "$INSTALL_JUGGERNAUT" != "1" ]; then
    warn "Smoke test skipped: default smoke uses JuggernautXL; selected profile does not install it."
    return
  fi
  if [ "$DRY_RUN" = "1" ]; then
    mkdir -p "$RUNTIME/commercial-image-runtime-tests/router-regression"
    python3 - <<PY
import pathlib, zlib, struct
out = pathlib.Path('$RUNTIME') / 'commercial-image-runtime-tests/router-regression/router_regression_bg_00001_.png'
width, height = 16, 16
raw = b''.join([b'\x00' + bytes([200, 200, 200]) * width for _ in range(height)])
def chunk(t, d):
    c = t + d
    return struct.pack('>I', len(d)) + c + struct.pack('>I', zlib.crc32(c) & 0xFFFFFFFF)
with out.open('wb') as f:
    f.write(b'\x89PNG\r\n\x1a\n')
    f.write(chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)))
    f.write(chunk(b'IDAT', zlib.compress(raw)))
    f.write(chunk(b'IEND', b''))
print(out)
PY
    warn "[dry-run] wrote placeholder smoke-test artifact"
    return
  fi
  log "Running JuggernautXL smoke test through ComfyUI API"
  if ! curl -sS --max-time 3 http://127.0.0.1:8188/system_stats >/dev/null; then
    "$RUNTIME/start_comfy.sh" > "$RUNTIME/comfy.log" 2>&1 &
    pid=$!
    for _ in $(seq 1 60); do
      if curl -sS --max-time 3 http://127.0.0.1:8188/system_stats >/dev/null; then break; fi
      sleep 2
    done
    curl -sS --max-time 3 http://127.0.0.1:8188/system_stats >/dev/null || { tail -80 "$RUNTIME/comfy.log"; fail "ComfyUI did not start"; }
    echo "$pid" > "$RUNTIME/comfy.pid"
  fi
  "$RUNTIME/run_smoke_test.sh"
}

main(){
  log "Installing AI图片制作 runtime profile=$PROFILE"
  log "HERMES_HOME=$HERMES_HOME"
  log "HERMES_IMAGE_RUNTIME=$RUNTIME"
  install_skill
  if [ "$INSTALL_SKILL_ONLY" = "1" ]; then
    log "Skill-only install complete. Runtime install skipped."
    return
  fi
  install_system_deps
  if [ "$INSTALL_COMFY_STACK" = "1" ]; then
    install_uv
    install_comfy
    install_helpers
    install_models
    write_launcher
  fi
  install_layout
  run_smoke
  log "Done. In Hermes: /reload-skills then /skill commercial-image-router"
  log "ComfyUI launcher: $RUNTIME/start_comfy.sh"
}

main "$@"
