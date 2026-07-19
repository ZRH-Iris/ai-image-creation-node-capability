1|# Technical Notes
2|
3|普通用户不需要阅读这个文件。这里是给部署人员/技术人员看的细节。
4|
5|## Full install
6|
7|```bash
8|bash setup_runtime.sh
9|```
10|
11|Default install paths:
12|
13|```text
14|Skill:   ~/.hermes/skills/creative/commercial-image-router
15|Runtime: ~/.hermes-image-runtime
16|```
17|
18|Custom paths:
19|
20|```bash
21|HERMES_HOME=/path/to/.hermes \
22|HERMES_IMAGE_RUNTIME=/data/hermes-image-runtime \
23|bash setup_runtime.sh
24|```
25|
26|HuggingFace mirror:
27|
28|```bash
29|HF_ENDPOINT=https://hf-mirror.com bash setup_runtime.sh
30|```
31|
32|## Lightweight skill-only install
33|
34|For testing package structure only:
35|
36|```bash
37|bash setup_runtime.sh --install-skill-only
38|```
39|
40|This does not install ComfyUI or models and will not reproduce image quality.
41|
42|## What setup_runtime.sh installs
43|
44|- commercial-image-router Skill
45|- system deps when apt is available: git, curl, nodejs, npm, Noto CJK fonts
46|- uv
47|- ComfyUI
48|- Python venv
49|- PyTorch
50|- ComfyUI requirements
51|- segment-anything, opencv-python-headless, pycocotools, pillow, numpy
52|- Node project with sharp and @resvg/resvg-js
53|- ComfyUI helper scripts/workflows
54|- model files listed in runtime_manifest.json
55|- start_comfy.sh
56|- run_smoke_test.sh
57|
58|## Models
59|
60|The installer downloads:
61|
62|- Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors
63|- sd_xl_base_1.0.safetensors
64|- sam_vit_b_01ec64.pth
65|- 4x-UltraSharp.pth
66|
67|## After install
68|
69|Start ComfyUI manually if needed:
70|
71|```bash
72|~/.hermes-image-runtime/start_comfy.sh
73|```
74|
75|Run smoke test:
76|
77|```bash
78|~/.hermes-image-runtime/run_smoke_test.sh
79|```
80|
81|Load the skill in Hermes/Harness:
82|
83|```text
84|/reload-skills
85|/skill commercial-image-router
86|```
87|
88|## Environment variables
89|
90|- `HERMES_HOME`: where the Skill is installed.
91|- `HERMES_IMAGE_RUNTIME`: runtime root for ComfyUI/models/output.
92|- `HF_ENDPOINT`: optional HuggingFace mirror.
93|- `COMFY_HELPERS_DIR`: optional helper script directory for audit.
94|- `COMFY_WORKSPACE`: optional ComfyUI workspace path.
95|
96|## Known limitations
97|
98|- Requires stable internet for large model downloads.
99|- NVIDIA GPU strongly recommended.
100|- GPT/Gemini/Figma/Canva integrations are not included; this package focuses on the local ComfyUI-based route.
101|- Advanced text removal and complex object editing may require later IOPaint/LaMA/BrushNet integration.
102|

## Self-test dry-run mode

The installer includes `--dry-run`. This mode copies the Skill, installs helpers, creates the expected folder structure, writes launcher scripts, and generates a placeholder smoke-test PNG without cloning ComfyUI, installing packages, or downloading models. It is useful for validating the package itself on a new machine.

```bash
bash setup_runtime.sh --dry-run
```
