# 模型选择与安装 Profile 定稿

本参考记录 AI图片制作 Skill 的当前产品决策。结论来自本机实测：同一批任务分别用 Qwen-Image-2512、JuggernautXL v9、SDXL Base 以及旧版低质模型直出生成古诗图、北京夏令营海报、小红书正能量封面后对比。

## 最终模型定位

### 主模型：JuggernautXL v9

默认主生图模型是 JuggernautXL v9。

适合：

- 高质感主视觉；
- 商业摄影感背景；
- 产品氛围图；
- 小红书生活方式图；
- 活动/宣传/海报的无字背景；
- 一般“帮我生成一张好看的图”。

原因：

- 实测部分画面比 Qwen 更好看、更成熟；
- 模型体积比 Qwen 小很多，约 6.7GB；
- ComfyUI/SDXL 生态成熟；
- 适合作为普通用户第一可用生图底座。

限制：

- 不擅长可靠中文文字；
- 不能直接承担复杂中文海报文字；
- 有字成品必须用 layout/模板层兜底。

### 中文增强/备选：Qwen-Image-2512

Qwen 不是默认主模型，但在中文场景中是强备选，某些场景可以直接够用。

适合：

- 短中文小红书图；
- 正能量短句图；
- 古诗/中文文化意境图初稿；
- 用户明确要求“单模型自己写中文”；
- 中文语义理解更重要的创意图；
- 后续 Qwen-Image-Edit 类指令改图。

限制：

- 体积大，约 30GB+；
- 复杂长文案仍可能错字/字形不稳；
- 画面商业质感并非总是超过 JuggernautXL。

### 兼容兜底：SDXL Base

SDXL Base 只作为兼容/基准/fallback。普通安装不默认下载。

适合：

- 某些 SDXL workflow 需要基础模型；
- 兼容测试；
- JuggernautXL 下载失败时的 fallback。

### 删除：SD1.5

SD1.5 不进入正式安装和推荐路线。它只保留在历史测试认知中，不作为 AI图片制作 Skill 的候选模型。

## 为什么默认要安装 ComfyUI？

ComfyUI 不是最终用户要学习的软件，也不是 Skill 的卖点。它是本地模型运行器。

Hermes 本身负责理解需求、调用工具、质检和交付；但 JuggernautXL、Qwen、SDXL 这些开放权重模型不能直接在 Hermes 文本对话里运行，需要一个本地推理后端。

ComfyUI 在本 Skill 中负责：

1. 加载 JuggernautXL/Qwen/SDXL 模型；
2. 执行 txt2img/img2img/inpaint/upscale 等 workflow；
3. 提供本地 API `http://127.0.0.1:8188`，让 Hermes 自动调用；
4. 保存输出图片，供 Hermes 检查和发送；
5. 未来扩展商品图、改图、放大、模板化 workflow。

对用户来说，不需要打开或学习 ComfyUI；它只是底层引擎。

## 安装 Profiles

### 默认：core-generate

执行：

```bash
python3 installer/install_commercial_image_router.py
```

默认等同：

```bash
python3 installer/install_commercial_image_router.py --profile core-generate
```

安装：

- `commercial-image-router` Skill；
- ComfyUI；
- PyTorch；
- JuggernautXL v9；
- 基础 txt2img workflow；
- smoke test。

不安装：

- Qwen；
- SDXL Base；
- 旧版低质模型；
- SAM；
- 4x-UltraSharp；
- 商品图/放大修复全家桶。

这是“拿到链接后直接能生图”的最小实用包。

### skill-only

只装 Skill 和规则，不装模型。适合已有图片 API 或自带 ComfyUI 的用户。

### qwen

安装 Qwen-Image-2512 模型与 workflow。仅在需要中文短文案、古诗、中文文化图、模型本身写中文、中文指令改图时按需安装。

### creator

安装 JuggernautXL + Qwen + layout。适合重度做图用户，但体积较大。

### layout

安装 Node/SVG 中文排版层。用于最终准确中文标题、活动信息、古诗题跋、商品卖点。不依赖模型生成文字。

### sdxl-base

安装 SDXL Base 兼容模型。只做 workflow 兼容/fallback。

### full

安装 creator + SDXL Base。后续商品图/SAM/放大修复继续按需扩展，不作为默认安装。

## 路由规则

| 场景 | 首选 | 说明 |
|---|---|---|
| 普通好看图/商业主视觉/背景 | JuggernautXL | 默认主模型。 |
| 商品氛围图 | JuggernautXL | 商品主体必须单独保留，不能让模型重画。 |
| 活动/招生/夏令营海报 | JuggernautXL + layout | 主视觉用 JuggernautXL，时间地点行程由 layout 精确渲染。 |
| 小红书短句图 | Qwen 或 JuggernautXL | Qwen 可直接写短中文；若追求更强质感，用 JuggernautXL 背景 + layout。 |
| 古诗图/中文文化图 | Qwen 先试；成品 layout 兜底 | Qwen 懂中文意境；完整诗文最终应确定性排版。 |
| 用户要求模型本身写中文 | Qwen | 明确说明可能有错字风险。 |
| 兼容测试 | SDXL Base | 不作为主模型。 |

## 验证规则

安装器必须：

1. 明确输出当前 profile；
2. 安装完成后运行 smoke test，除非用户传 `--no-smoke-test`；
3. smoke test 默认使用 JuggernautXL 生成无字图，验证 ComfyUI/PyTorch/model/workflow 链路；
4. dry-run 必须生成占位 smoke artifact，验证安装路径和文件结构；
5. GitHub 发布后必须验证公开仓库、raw README、raw AUTO_INSTALL、raw installer、raw Skill 可访问；
6. 必须再从 raw installer 下载到临时 Hermes 环境执行 `--dry-run` 验证，不能只本地通过。
