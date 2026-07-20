# AI图片制作能力｜转发给 Hermes/节点自动安装

这是一个可以转发给 Hermes/节点的图片生成与处理能力安装入口。

用户把本 GitHub 链接发给自己的 Hermes 后，Hermes 应读取 `AUTO_INSTALL_FOR_HERMES.md` 并执行安装，不要只总结内容。

## 默认会先安装什么？

默认安装的是 **core-generate** 基础生图包，不是几十 GB 全家桶。

默认安装内容：

1. `commercial-image-router` Skill：图片制作路由、模型选择、质量检查规则；
2. ComfyUI：本地模型运行器/API 层；
3. PyTorch：运行本地生图模型需要的推理框架；
4. JuggernautXL v9：默认主生图模型，约 6.7GB；
5. 基础 txt2img workflow：让 Hermes 能通过 ComfyUI 直接生成图片；
6. smoke test：安装后自动生成一张无字测试图，验证模型/ComfyUI/workflow 链路真的可用。

默认不安装：

- Qwen-Image-2512：体积约 30GB+，只在中文短文案/古诗/模型本身写中文/中文指令场景按需安装；
- SDXL Base：只作为兼容 fallback；
- SD1.5：已从正式方案删除；
- SAM、4x-UltraSharp、商品图/放大修复全家桶：后续按需扩展，不默认塞入。

## 为什么需要 ComfyUI？

ComfyUI 不是让普通用户学习的软件，它只是底层本地模型运行器。

Hermes 负责理解你的需求、选择路线、调用工具、检查结果、发送图片；但 JuggernautXL、Qwen 这类开放权重模型需要一个运行后端来加载模型、执行 workflow、输出图片。ComfyUI 就负责这个底层工作，并通过本地 API 给 Hermes 调用。

用户正常使用时只需要说：

```text
帮我做一张小红书图
帮我做一张宣传海报
帮我生成一张商品氛围图
```

不需要打开或学习 ComfyUI。

## 推荐安装方式：GitHub 链接安装

把这个仓库链接直接转发给 Hermes：

```text
请读取并严格执行这个能力，为我安装“AI图片制作”。不要只总结内容，安装完成后主动告诉我如何上传图片和需求来生成/修改图片：
https://github.com/ZRH-Iris/ai-image-creation-node-capability
```

Hermes 收到后应该：

1. 读取 `AUTO_INSTALL_FOR_HERMES.md`；
2. 执行 `installer/install_commercial_image_router.py`；
3. 默认安装 core-generate 基础生图包；
4. 自动安装 ComfyUI/PyTorch/JuggernautXL/workflow；
5. 自动运行 smoke test；
6. 用普通用户能听懂的话告诉用户下一步怎么使用。

## 安装命令

默认安装 core-generate：

```bash
python3 installer/install_commercial_image_router.py
```

只安装 Skill，不装模型：

```bash
python3 installer/install_commercial_image_router.py --profile skill-only
```

按需安装 Qwen 中文增强：

```bash
python3 installer/install_commercial_image_router.py --profile qwen
```

安装 JuggernautXL + Qwen + layout：

```bash
python3 installer/install_commercial_image_router.py --profile creator
```

备用 raw 安装：

```bash
python3 - <<'PY'
import urllib.request, tempfile, subprocess, pathlib
url = 'https://raw.githubusercontent.com/ZRH-Iris/ai-image-creation-node-capability/main/installer/install_commercial_image_router.py'
p = pathlib.Path(tempfile.gettempdir()) / 'install_commercial_image_router.py'
p.write_text(urllib.request.urlopen(url).read().decode('utf-8'), encoding='utf-8')
subprocess.run(['python3', str(p)], check=True)
PY
```

## 安装后怎么使用

安装完成后，用户可以直接对 Hermes 说：

```text
帮我做一张封面图。
```

```text
我发一张商品图，请帮我做成商品宣传海报。
```

```text
帮我做一张活动宣传图，标题是……，文案是……
```

## 模型选择逻辑

- 默认好看图/商业主视觉/产品氛围图：JuggernautXL；
- 短中文小红书图/古诗图/用户要求模型自己写中文：Qwen，按需安装；
- 活动/招生/夏令营海报：JuggernautXL 出主视觉，准确文字应由 layout/模板层兜底；
- SDXL Base：兼容 fallback；
- 旧版低质模型：不使用。

## 重要说明

- 商品图默认保留真实商品主体，不随便重画商品、Logo、包装和颜色。
- 中文标题和文案如果必须准确，不能完全依赖模型直接生成，应由排版层处理。
- 对外发布图片必须检查清晰度、裁切、文字可读性和主体是否变形。
- 不适合用来制作冒充他人、侵权或欺骗性质的图片。
