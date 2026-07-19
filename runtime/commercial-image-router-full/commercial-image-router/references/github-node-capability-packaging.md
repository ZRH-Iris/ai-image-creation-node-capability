# GitHub node-capability packaging pattern

Use when the user wants to publish the commercial image router as a shareable GitHub link that other Hermes/Harness users can forward to their own node for automatic installation.

## Intent

The user wants a **GitHub-distributed capability**, not just a tarball and not a technical repository. The target recipient may be non-technical and should be able to send a GitHub link to Hermes with an instruction like “读取并严格执行这个能力，为我安装……”.

## Required repository shape

Mirror the proven capability pattern:

```text
commercial-image-router-node-capability/
├── README.md
├── AUTO_INSTALL_FOR_HERMES.md
├── MANIFEST.yaml
├── installer/
│   └── install_commercial_image_router.py
├── runtime/
│   └── commercial-image-router-full/
├── docs/
│   └── USER_GUIDE.md
└── card/
    └── feishu_forward_card.md
```

### README.md

For ordinary users. Explain what the capability does and show the GitHub-link installation prompt. Do not expose model names, checkpoint names, PyTorch internals, ComfyUI internals, or long terminal logs in the primary README.

### AUTO_INSTALL_FOR_HERMES.md

For Hermes. It must explicitly instruct Hermes to:

1. read `README.md`, `MANIFEST.yaml`, and the installer;
2. run `python3 installer/install_commercial_image_router.py`;
3. install Skill + runtime + models/fonts/helpers/workflows;
4. run verification/smoke test;
5. reply with a simple usage explanation.

### MANIFEST.yaml

Machine-readable summary: name, display name, version, description, entry, installer, runtime, skill name, trigger examples, required inputs, safety notes, and routing notes.

### installer/

The installer should locate local runtime files when cloned, or download the repo archive when invoked from a raw installer. It should support environment overrides for debugging (`COMMERCIAL_IMAGE_ROUTER_INSTALL_ARGS`, `HERMES_HOME`, `HERMES_IMAGE_RUNTIME`) but hide that from ordinary users.

### runtime/

Embed the already-tested full runtime package directory, not only SKILL.md. The promise is “install this GitHub capability and get the actual image-processing ability,” so include the full `commercial-image-router-full/` runtime with `setup_runtime.sh`, helper workflows/scripts, templates, model manifest, and smoke-test logic.

## Mandatory self-test before publishing

Before saying the GitHub repo is ready:

```bash
python3 -m py_compile installer/install_commercial_image_router.py
bash -n runtime/commercial-image-router-full/setup_runtime.sh
bash -n runtime/commercial-image-router-full/一键安装.sh
rm -rf /tmp/image-router-gh-test-home /tmp/image-router-gh-test-runtime
HERMES_HOME=/tmp/image-router-gh-test-home \
HERMES_IMAGE_RUNTIME=/tmp/image-router-gh-test-runtime \
COMMERCIAL_IMAGE_ROUTER_INSTALL_ARGS='--dry-run' \
python3 installer/install_commercial_image_router.py
```

Then verify all of these exist:

```text
/tmp/image-router-gh-test-home/skills/creative/commercial-image-router/SKILL.md
/tmp/image-router-gh-test-runtime/comfy-helpers/scripts/run_workflow.py
/tmp/image-router-gh-test-runtime/comfy-helpers/workflows/sdxl_txt2img.json
/tmp/image-router-gh-test-runtime/start_comfy.sh
/tmp/image-router-gh-test-runtime/run_smoke_test.sh
/tmp/image-router-gh-test-runtime/commercial-image-runtime-tests/router-regression/router_regression_bg_00001_.png
```

Also check the PNG header starts with `89 50 4E 47 0D 0A 1A 0A`.

## Pitfalls from the packaging session

- If the user gives another capability repo as an **example**, do not execute its installer unless the user explicitly asks to install that capability. Study its structure and apply the pattern to the image capability.
- Do not confuse “reference this case” with “install this case”. If the user says “参考这个来做我们这个,” stop any example installation path and return to packaging the image Skill.
- `gh` may be absent and GitHub credentials may be missing. Build and commit the local repo anyway, then ask for either an empty GitHub repo URL or a one-time token. Do not invent that the push succeeded.
- Use local git config for generated repos (`git config user.name`, `git config user.email`) instead of changing global config.
- Keep placeholder GitHub URLs (`YOUR_GITHUB_USERNAME`) clearly visible until the final remote URL is known. After the remote is known, replace placeholders in README, AUTO_INSTALL, MANIFEST/card docs, and installer default archive URL.
