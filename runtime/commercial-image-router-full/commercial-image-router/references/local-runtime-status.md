# AI图片制作：当前本机高质量能力验收记录

更新时间：2026-07-20

## 当前定稿路线

本 Skill 已从“图片工具全家桶”调整为清晰的 AI 图片制作路由器：

- 默认安装：`core-generate`
- 默认主模型：JuggernautXL v9
- 默认安装内容：ComfyUI + PyTorch + JuggernautXL + 基础 SDXL/JuggernautXL txt2img workflow + smoke test
- Qwen：不默认安装，作为中文短文案、古诗图、模型直写中文、中文指令理解/编辑的按需增强 profile
- SDXL Base：兼容/兜底 profile
- 旧版低质模型：不进入正式安装和推荐路线

## 为什么默认装 ComfyUI

JuggernautXL 和 Qwen 都不是 Hermes 内置模型。它们需要一个本地模型运行器来：

1. 加载模型 checkpoint / diffusion model / VAE / LoRA；
2. 执行 txt2img、img2img、inpaint、upscale 等 workflow；
3. 暴露本地 API，供 Hermes 自动提交任务并取回图片；
4. 让用户不必手动学习 ComfyUI，Hermes 只把它当后端。

因此默认 core-generate 会安装 ComfyUI。不是让用户去操作 ComfyUI，而是让 Hermes 有一个稳定的本地生图引擎。

## 本机算力确认

实时检查结果：

- GPU：NVIDIA GeForce RTX 5090 × 2
- 单卡显存：约 31.8GB
- 总显存：约 63.6GB
- CPU：AMD Ryzen 9 9950X3D，16 核 32 线程
- RAM：59GB
- `/opt/data` 剩余磁盘：约 383GB
- Torch：`2.13.0+cu130`
- CUDA available：True
- CUDA device count：2

结论：本机足够跑 JuggernautXL、SDXL Base、Qwen-Image-2512；Qwen 和大模型建议串行运行，不建议多模型并发。

## 已验证：Skill / Runtime 审计

命令：

```bash
HERMES_IMAGE_RUNTIME=/opt/data /opt/hermes/.venv/bin/python runtime/commercial-image-router-full/commercial-image-router/scripts/audit_skill.py runtime/commercial-image-router-full/commercial-image-router
HERMES_IMAGE_RUNTIME=/opt/data /opt/hermes/.venv/bin/python runtime/commercial-image-router-full/commercial-image-router/scripts/audit_runtime.py runtime/commercial-image-router-full
```

结果：

```text
skill ok= True failed= 0 missing= []
runtime ok= True failed= 0 missing= []
```

## 已验证：JuggernautXL core-generate smoke test

命令使用默认 SDXL/JuggernautXL workflow：

```bash
/opt/data/comfy-venv/bin/python runtime/commercial-image-router-full/comfy-helpers/scripts/run_workflow.py \
  --workflow runtime/commercial-image-router-full/comfy-helpers/workflows/sdxl_txt2img.json \
  --args '{"ckpt_name":"Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors","prompt":"premium warm lifestyle poster background, commercial photography, clean composition, no text, no watermark","negative_prompt":"text, letters, watermark, logo, blurry, deformed, low quality","width":768,"height":960,"steps":12,"cfg":6,"sampler_name":"dpmpp_2m","scheduler":"karras","seed":20260720,"filename_prefix":"skill_core_juggernaut_smoke"}' \
  --output-dir /opt/data/ai-image-skill-verify/juggernaut_smoke
```

输出：

```text
/opt/data/ai-image-skill-verify/juggernaut_smoke/skill_core_juggernaut_smoke_00001_.png
```

视觉 QA：

- 成功生成暖色商业生活方式/摄影感背景；
- 无文字；
- 无水印；
- 无乱码；
- 无明显坏图；
- 证明 core-generate 的 JuggernautXL txt2img 链路真实跑通。

## 已验证：dry-run 安装

已用临时 `HERMES_HOME` 和 `HERMES_IMAGE_RUNTIME` 跑过安装器 dry-run：

```bash
/opt/hermes/.venv/bin/python installer/install_commercial_image_router.py --dry-run
```

确认生成：

- `skills/creative/commercial-image-router/SKILL.md`
- `references/model-selection-and-install-profiles.md`
- `start_comfy.sh`
- `run_smoke_test.sh`
- placeholder smoke artifact

## 待完成

- GitHub commit/push
- 公共 GitHub 链接验证
- raw 安装命令验证
- 最终把可转发安装话术发给用户
