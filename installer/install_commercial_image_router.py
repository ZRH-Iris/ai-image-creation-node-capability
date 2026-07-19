#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path

CAPABILITY_NAME = 'AI图片制作'
VERSION = '1.0.0'
DEFAULT_ARCHIVE_URL = 'https://github.com/ZRH-Iris/ai-image-creation-node-capability/archive/refs/heads/main.tar.gz'


def say(msg: str):
    print(msg, flush=True)


def run(cmd, cwd=None, env=None, quiet=False):
    if quiet:
        return subprocess.run(cmd, cwd=cwd, env=env, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return subprocess.run(cmd, cwd=cwd, env=env, check=True)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def runtime_dir_from_local() -> Path | None:
    root = repo_root()
    candidate = root / 'runtime' / 'commercial-image-router-full'
    if (candidate / 'setup_runtime.sh').exists():
        return candidate
    return None


def download_repo_runtime() -> Path:
    url = os.environ.get('COMMERCIAL_IMAGE_ROUTER_REPO_ARCHIVE', DEFAULT_ARCHIVE_URL)
    tmp = Path(tempfile.mkdtemp(prefix='commercial-image-router-install-'))
    archive = tmp / 'repo.tar.gz'
    say('正在获取安装文件，请稍等。')
    urllib.request.urlretrieve(url, archive)
    with tarfile.open(archive, 'r:gz') as tf:
        tf.extractall(tmp)
    matches = list(tmp.glob('*/runtime/commercial-image-router-full/setup_runtime.sh'))
    if not matches:
        raise RuntimeError('安装包结构不完整，找不到图片处理运行环境。')
    return matches[0].parent


def find_runtime_dir() -> Path:
    local = runtime_dir_from_local()
    if local:
        return local
    return download_repo_runtime()


def install():
    say('收到，正在为你安装「AI图片制作」能力。')
    say('我会自动完成准备和验证，你暂时不需要做任何技术操作。')
    runtime = find_runtime_dir()
    setup = runtime / 'setup_runtime.sh'
    if not setup.exists():
        raise RuntimeError('找不到安装脚本。')
    os.chmod(setup, 0o755)
    env = os.environ.copy()
    env.setdefault('COMMERCIAL_IMAGE_ROUTER_SOURCE', str(repo_root()))
    # 默认完整安装；如调试可由环境变量传入额外参数。
    extra = env.get('COMMERCIAL_IMAGE_ROUTER_INSTALL_ARGS', '').split()
    if env.get('COMMERCIAL_IMAGE_RUNTIME_DRY_RUN') == '1' and '--dry-run' not in extra:
        extra.append('--dry-run')
    cmd = ['bash', str(setup)] + extra
    run(cmd, cwd=str(runtime), env=env, quiet=False)
    say('')
    say('「AI图片制作」已经安装成功，可以开始使用了。')
    say('')
    say('接下来你可以直接发给我：')
    say('1. 一张要处理的图片，或一句想生成图片的需求；')
    say('2. 标题、文案、尺寸或风格要求；')
    say('3. 如果是商品图，请尽量发清晰原图，并说明哪些内容必须保持不变。')
    say('')
    say('你可以这样说：')
    say('“我发一张商品图，请帮我做成宣传海报，商品不要变形。”')
    say('或者：')
    say('“帮我做一张活动海报，标题是……，文案是……。”')
    say('')
    say('以后再次使用时，不需要重新安装，直接说你的图片需求即可。')


def main():
    try:
        install()
    except Exception as e:
        print('', file=sys.stderr)
        print('「AI图片制作」暂时没有安装成功。', file=sys.stderr)
        print('原因：' + str(e), file=sys.stderr)
        print('你可以把这段失败提示转发给我，我会继续帮你处理。', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
