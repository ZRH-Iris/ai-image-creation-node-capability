# Runtime Distribution Packaging

Use this reference when the user asks to share `commercial-image-router` with other Hermes/Harness users. The target is not a developer-only Skill archive; the target is a normal-user install package that reproduces the runtime quality as much as possible.

## Core lesson from user correction

The user does **not** want to hand other people a technical bundle that merely documents the workflow. The user wants other, often non-technical, people to install one package and then use Hermes/Harness normally for high-quality image work.

Therefore, a shareable package must include:

1. The Skill directory.
2. The installer for the full runtime.
3. Helper ComfyUI workflows/scripts.
4. Model download manifest and download logic.
5. Font installation.
6. Segmentation support.
7. Upscale support.
8. Smoke test after install.
9. A plain-language README for non-technical users.
10. Technical details separated into `TECHNICAL.md`, not exposed in the main README.

## Package shape

Preferred package root:

```text
commercial-image-router-full/
├── README.md                  # ordinary user instructions only
├── 一键安装.sh                 # one command / one double-click style entrypoint
├── setup_runtime.sh           # real installer, technical but hidden from normal user flow
├── TECHNICAL.md               # details for technical support/debugging
├── runtime_manifest.json      # model URLs, paths, hashes
├── commercial-image-router/   # Skill directory
└── comfy-helpers/             # workflows and helper scripts
```

Do **not** ship only `commercial-image-router/` when the user asks for a package others can install to get the same image quality. That only shares process knowledge, not capability.

## README rule for non-technical users

The public `README.md` should be short and operational:

- Say what it enables in normal language: generate images, product posters, Xiaohongshu covers, avatars, background changes, upscaling, basic edits.
- Show only the command:

```bash
bash 一键安装.sh
```

- Explain that installation may take a long time because image models download.
- Give only one troubleshooting fallback for slow model downloads:

```bash
HF_ENDPOINT=https://hf-mirror.com bash 一键安装.sh
```

- Mention that an NVIDIA GPU is recommended.

Avoid exposing model/tool jargon in README: ComfyUI, SAM, Juggernaut, SDXL, checkpoint, manifest, PyTorch. Put those in `TECHNICAL.md`.

## Installer defaults

`bash 一键安装.sh` must perform the full install by default:

- install Skill into `$HERMES_HOME/skills/creative/commercial-image-router`;
- install/clone ComfyUI;
- create Python venv;
- install PyTorch and ComfyUI dependencies;
- install SAM/segmentation deps;
- install Node/sharp SVG layout layer;
- install CJK fonts where possible;
- download required models;
- write launch scripts;
- start ComfyUI if needed;
- run a smoke test image generation.

A skill-only mode is acceptable for QA/testing, but it must not be the advertised normal-user path because it does not reproduce quality:

```bash
bash setup_runtime.sh --install-skill-only
```

## Portability rules

Do not hardcode origin-machine paths in distributed scripts. Use environment variables with sensible defaults:

- `HERMES_HOME`, default `$HOME/.hermes`.
- `HERMES_IMAGE_RUNTIME`, default `$HOME/.hermes-image-runtime`.
- `COMFY_HELPERS_DIR`, default `$HERMES_IMAGE_RUNTIME/comfy-helpers`.
- `COMFY_WORKSPACE`, default `$HERMES_IMAGE_RUNTIME/comfy-workspace`.
- `HF_ENDPOINT`, optional HuggingFace mirror.

Origin-machine verification evidence may live in `references/local-runtime-status.md`, but the main `SKILL.md` and distributed scripts must use portable environment variables such as `$HERMES_IMAGE_RUNTIME` / `$HERMES_HOME`, not developer-machine absolute paths.

## Mandatory package QA before sending

Before sending a package to the user, run these checks on the tarball contents, not only the source directory:

1. Extract into a fresh temporary directory.
2. Verify there is no duplicate nested Skill directory, especially:

```text
commercial-image-router/commercial-image-router/
```

3. Remove caches before packing:

```bash
find commercial-image-router-full -type d -name __pycache__ -prune -exec rm -rf {} +
find commercial-image-router-full -type f \( -name '*.pyc' -o -name '.DS_Store' \) -delete
```

4. Check shell syntax:

```bash
bash -n setup_runtime.sh
bash -n 一键安装.sh
```

5. Check Python scripts:

```bash
python -m py_compile commercial-image-router/scripts/*.py comfy-helpers/scripts/*.py
```

6. Check Node scripts:

```bash
node --check commercial-image-router/scripts/compose_product_poster.js
```

7. Run a temporary install rehearsal without downloading models:

```bash
HERMES_HOME=/tmp/commercial-image-router-home \
HERMES_IMAGE_RUNTIME=/tmp/commercial-image-router-runtime \
bash setup_runtime.sh --install-skill-only
```

8. Verify installed Skill exists and is not nested:

```text
/tmp/commercial-image-router-home/skills/creative/commercial-image-router/SKILL.md
```

9. Run runtime audit on the source machine when possible:

```bash
COMFY_HELPERS_DIR=/path/to/comfy-helpers \
HERMES_IMAGE_RUNTIME=/path/to/runtime \
python commercial-image-router/scripts/audit_skill.py
```

## Common packaging pitfall

If you copy the Skill directory into an existing package folder without deleting the old copy first, you can accidentally create:

```text
commercial-image-router/commercial-image-router/
```

Always `rm -rf package/commercial-image-router` before copying the latest Skill.

## Versioning guidance

When a package fails QA, do not tell the user it is ready. Create a new version and clearly mark the older version as not recommended. In the session that created this reference, v3 failed due to duplicate nesting and old hardcoded audit paths; v4 became the corrected share candidate after fixing those issues and re-running checks.
