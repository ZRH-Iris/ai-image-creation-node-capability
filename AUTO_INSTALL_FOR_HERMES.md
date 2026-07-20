# 节点引擎丨AI图片制作自动安装能力

请读取并严格执行本安装说明，为当前 Hermes/节点安装“AI图片制作”能力。不要只总结内容。收到本链接即表示用户希望立即安装基础生图能力。

## 本次默认安装目标

默认安装 **core-generate**，也就是先让用户真正能生图：

1. 安装 `commercial-image-router` Skill；
2. 安装 ComfyUI 作为本地模型运行器；
3. 安装 PyTorch；
4. 下载并安装默认主模型 JuggernautXL v9；
5. 安装基础 txt2img workflow；
6. 运行 smoke test，确认可以通过 ComfyUI API 生成一张测试图；
7. 用普通用户能听懂的话告诉用户安装成功后怎么使用。

默认不安装 Qwen。Qwen 体积约 30GB+，只在用户需要中文短文案、古诗图、模型本身写中文、中文文化场景或 Qwen-Image-Edit 类改图时，再按需执行：

```bash
python3 installer/install_commercial_image_router.py --profile qwen
```

SD1.5 已从正式方案删除，不要安装。

## 为什么要装 ComfyUI

ComfyUI 不是给用户学习的软件，它只是底层运行器。

Hermes 负责理解需求、选模型、质检和发送图片；JuggernautXL/Qwen 这类开放权重模型需要本地推理后端来加载模型、运行 workflow、输出图片。ComfyUI 提供这个本地 API 层。

安装后用户不需要打开 ComfyUI，只需要继续在 Hermes 里说图片需求。

## 立即执行

请按顺序执行：

1. 打开当前 GitHub 仓库；
2. 读取 `README.md`、`MANIFEST.yaml` 和 `installer/install_commercial_image_router.py`；
3. 执行默认安装脚本：

```bash
python3 installer/install_commercial_image_router.py
```

如果当前环境无法从相对路径执行，请先克隆仓库后执行：

```bash
git clone https://github.com/ZRH-Iris/ai-image-creation-node-capability.git
cd ai-image-creation-node-capability
python3 installer/install_commercial_image_router.py
```

如果用户发送的是 raw 链接，可用以下方式直接安装：

```bash
python3 - <<'PY'
import urllib.request, tempfile, subprocess, pathlib
url = 'https://raw.githubusercontent.com/ZRH-Iris/ai-image-creation-node-capability/main/installer/install_commercial_image_router.py'
p = pathlib.Path(tempfile.gettempdir()) / 'install_commercial_image_router.py'
p.write_text(urllib.request.urlopen(url).read().decode('utf-8'), encoding='utf-8')
subprocess.run(['python3', str(p)], check=True)
PY
```

## 可选安装 profile

默认：

```bash
python3 installer/install_commercial_image_router.py
```

等同：

```bash
python3 installer/install_commercial_image_router.py --profile core-generate
```

只安装 Skill：

```bash
python3 installer/install_commercial_image_router.py --profile skill-only
```

按需安装 Qwen：

```bash
python3 installer/install_commercial_image_router.py --profile qwen
```

安装 JuggernautXL + Qwen + layout：

```bash
python3 installer/install_commercial_image_router.py --profile creator
```

## 安装脚本必须完成的验证

安装脚本必须自动完成：

1. 输出正在安装的 profile；
2. 安装或更新 `commercial-image-router` Skill；
3. 安装 core-generate 所需运行环境；
4. 下载 JuggernautXL；
5. 写入启动脚本和 helper workflow；
6. 启动/连接 ComfyUI；
7. 通过基础 txt2img workflow 生成测试图；
8. 如果 smoke test 失败，不得假装成功。

## 成功后必须回复用户

安装成功后，请用普通用户能听懂的话主动回复，不要输出大段命令行日志、模型路径、配置文件路径等技术细节。

推荐回复：

「AI图片制作」基础生图能力已经安装成功，可以开始使用了。

现在默认可以使用 JuggernautXL 生成高质感图片。你可以直接发给我：
1. 一句想生成图片的需求；
2. 一张要处理的图片；
3. 标题、文案、尺寸或风格要求。

如果之后你要做短中文小红书图、古诗图，或者明确想让模型自己写中文，我会再按需安装 Qwen 中文增强能力。

## 失败时必须回复用户

如果安装失败，不要假装成功，也不要把大段技术日志发给普通用户。请用简单话说明是哪一类问题，例如：

- 当前环境缺少必要图片工具；
- 当前机器暂时带不动图片模型；
- 模型文件没有下载完整；
- 网络无法访问 GitHub 或模型源；
- 安装依赖时失败；
- 磁盘空间不足。

最后告诉用户：“你可以把这段失败提示转发给我，我会继续帮你处理。”

## 安全边界

不得用于制作冒充他人、侵权、欺骗身份、违法营销或未经授权使用他人肖像/品牌的图片。