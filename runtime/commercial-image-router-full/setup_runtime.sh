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
RUN_SMOKE=1
DOWNLOAD_MODELS=1
SKILL_ONLY=0
DRY_RUN=0

for arg in "$@"; do
  case "$arg" in
    --no-smoke-test) RUN_SMOKE=0 ;;
    --dry-run) DRY_RUN=1 ;;
    --skip-model-download) DOWNLOAD_MODELS=0 ;;
    --install-skill-only) SKILL_ONLY=1; RUN_SMOKE=0; DOWNLOAD_MODELS=0 ;;
    *) echo "Unknown option: $arg" >&2; exit 2 ;;
  esac
done

log(){ printf '\033[32m[commercial-image-runtime]\033[0m %s\n' "$*"; }
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
    warn "[dry-run] skipping apt installs and required command checks"
    return
  fi
  if command -v apt-get >/dev/null 2>&1; then
    if [ "$(id -u)" = "0" ]; then SUDO=""; else SUDO="sudo"; fi
    if command -v sudo >/dev/null 2>&1 || [ "$(id -u)" = "0" ]; then
      $SUDO apt-get update -qq || true
      $SUDO apt-get install -y -qq git curl ca-certificates nodejs npm fonts-noto-cjk fonts-noto-cjk-extra || true
      fc-cache -f || true
    else
      warn "apt found but sudo unavailable; install git/curl/node/npm/fonts-noto-cjk manually if missing."
    fi
  else
    warn "Non-apt system: install git, curl, node/npm, and Noto CJK fonts manually if missing."
  fi
  need_cmd git
  need_cmd curl
  need_cmd node
  need_cmd npm
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
    mkdir -p "$COMFY" "$VENV" "$RUNTIME/image-models/sam" "$RUNTIME/comfy-workspace/models/checkpoints" "$RUNTIME/comfy-workspace/models/upscale_models"
    warn "[dry-run] prepared placeholder ComfyUI directories without cloning or installing packages"
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
  log "Installing PyTorch (tries cu130, cu128, cu121, then default)"
  uv pip install --python "$VENV/bin/python" torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu130 \
    || uv pip install --python "$VENV/bin/python" torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128 \
    || uv pip install --python "$VENV/bin/python" torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 \
    || uv pip install --python "$VENV/bin/python" torch torchvision torchaudio
  log "Installing ComfyUI requirements"
  uv pip install --python "$VENV/bin/python" -r "$COMFY/requirements.txt"
  log "Installing SAM/segmentation Python deps"
  uv pip install --python "$VENV/bin/python" git+https://github.com/facebookresearch/segment-anything.git opencv-python-headless pycocotools pillow numpy
}

install_helpers(){
  log "Installing helper workflows/scripts into $HELPERS"
  mkdir -p "$HELPERS"
  rm -rf "$HELPERS/scripts" "$HELPERS/workflows"
  cp -a "$ROOT_DIR/comfy-helpers/scripts" "$HELPERS/scripts"
  cp -a "$ROOT_DIR/comfy-helpers/workflows" "$HELPERS/workflows"
  chmod +x "$HELPERS/scripts"/*.py || true
}

install_layout(){
  log "Installing Node/SVG layout runtime into $LAYOUT"
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
  if [ -n "$sha" ]; then
    echo "$sha  $dest" | sha256sum -c -
  fi
}

install_models(){
  if [ "$DOWNLOAD_MODELS" = "0" ]; then warn "Skipping model downloads"; return; fi
  download_file "JuggernautXL v9" "comfy-workspace/models/checkpoints/Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors" \
    "https://huggingface.co/RunDiffusion/Juggernaut-XL-v9/resolve/main/Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors?download=true" \
    "c9e3e68f89b8e38689e1097d4be4573cf308de4e3fd044c64ca697bdb4aa8bca"
  download_file "SDXL base fallback" "comfy-workspace/models/checkpoints/sd_xl_base_1.0.safetensors" \
    "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors?download=true" ""
  download_file "SAM ViT-B" "image-models/sam/sam_vit_b_01ec64.pth" \
    "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth" \
    "ec2df62732614e57411cdcf32a23ffdf28910380d03139ee0f4fcbe91eb8c912"
  download_file "4x-UltraSharp" "comfy-workspace/models/upscale_models/4x-UltraSharp.pth" \
    "https://huggingface.co/lokCX/4x-Ultrasharp/resolve/main/4x-UltraSharp.pth?download=true" \
    "a5812231fc936b42af08a5edba784195495d303d5b3248c24489ef0c4021fe01"
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
  --args '{"ckpt_name":"Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors","prompt":"premium clean snowy landscape background for children winter camp poster, bright safe cheerful atmosphere, no text, no watermark","negative_prompt":"text, watermark, letters, logo, scary, deformed, low quality","width":768,"height":960,"steps":12,"cfg":6,"sampler_name":"dpmpp_2m","scheduler":"karras","seed":20260719,"filename_prefix":"commercial_router_smoke"}' \
  --output-dir "$RUNTIME/smoke-test-output"
EOF
  chmod +x "$RUNTIME/run_smoke_test.sh"
}

run_smoke(){
  if [ "$RUN_SMOKE" = "0" ]; then return; fi
  if [ "$DRY_RUN" = "1" ]; then
    mkdir -p "$RUNTIME/commercial-image-runtime-tests/router-regression"
    python3 - <<PY
import pathlib, zlib, struct

out = pathlib.Path('$RUNTIME') / 'commercial-image-runtime-tests/router-regression/router_regression_bg_00001_.png'
width, height = 16, 16
r, g, b = 200, 200, 200

def chunk(chunk_type, data):
    c = chunk_type + data
    return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xFFFFFFFF)

with out.open('wb') as f:
    f.write(b'\x89PNG\r\n\x1a\n')
    f.write(chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)))
    raw = b''
    for _ in range(height):
        raw += b'\x00' + bytes([r, g, b]) * width
    f.write(chunk(b'IDAT', zlib.compress(raw)))
    f.write(chunk(b'IEND', b''))
print(out)
PY
    warn "[dry-run] wrote placeholder smoke-test artifact"
    return
  fi
  log "Running smoke test. Starting ComfyUI in background if needed."
  if ! curl -sS --max-time 3 http://127.0.0.1:8188/system_stats >/dev/null; then
    "$RUNTIME/start_comfy.sh" > "$RUNTIME/comfy.log" 2>&1 &
    pid=$!
    for i in $(seq 1 60); do
      if curl -sS --max-time 3 http://127.0.0.1:8188/system_stats >/dev/null; then break; fi
      sleep 2
    done
    curl -sS --max-time 3 http://127.0.0.1:8188/system_stats >/dev/null || { tail -80 "$RUNTIME/comfy.log"; fail "ComfyUI did not start"; }
    echo "$pid" > "$RUNTIME/comfy.pid"
  fi
  "$RUNTIME/run_smoke_test.sh"
}

main(){
  log "Installing commercial-image-router full runtime"
  log "HERMES_HOME=$HERMES_HOME"
  log "HERMES_IMAGE_RUNTIME=$RUNTIME"
  install_skill
  if [ "$SKILL_ONLY" = "1" ]; then
    log "Skill-only install complete. Full runtime install skipped by --install-skill-only."
    return
  fi
  install_system_deps
  install_uv
  install_comfy
  install_helpers
  install_layout
  install_models
  write_launcher
  run_smoke
  log "Done. In Hermes: /reload-skills then /skill commercial-image-router"
  log "Runtime launcher: $RUNTIME/start_comfy.sh"
}

main "$@"
