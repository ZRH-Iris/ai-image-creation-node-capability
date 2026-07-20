#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path

CAPABILITY_NAME = 'AI图片制作'
VERSION = '1.1.0'
DEFAULT_ARCHIVE_URL = 'https://github.com/ZRH-Iris/ai-image-creation-node-capability/archive/refs/heads/main.tar.gz'
VALID_PROFILES = {'skill-only', 'core-generate', 'layout', 'qwen', 'creator', 'sdxl-base', 'full'}


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


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Install AI图片制作 capability for Hermes.')
    parser.add_argument('--profile', default='core-generate', choices=sorted(VALID_PROFILES), help='Install profile. Default: core-generate')
    parser.add_argument('--dry-run', action='store_true', help='Simulate install without downloading large files')
    parser.add_argument('--no-smoke-test', action='store_true', help='Skip smoke test')
    parser.add_argument('--skip-model-download', action='store_true', help='Install runtime/workflows but skip model downloads')
    parser.add_argument('--install-skill-only', action='store_true', help='Compatibility alias for --profile skill-only')
    return parser.parse_args(argv)


def install(args: argparse.Namespace):
    profile = 'skill-only' if args.install_skill_only else args.profile
    say('收到，正在为你安装「AI图片制作」能力。')
    say(f'安装 profile：{profile}')
    if profile == 'core-generate':
        say('默认会安装 ComfyUI、PyTorch、JuggernautXL 和基础生图 workflow，并做 smoke test。')
        say('Qwen 不会默认安装；需要中文短文案/古诗/模型直写中文时可再按需安装。')
    elif profile == 'qwen':
        say('将安装 Qwen 中文增强能力，模型较大，约 30GB+。')
    elif profile == 'skill-only':
        say('将只安装 Skill/路由规则，不安装 ComfyUI 或模型。')
    runtime = find_runtime_dir()
    setup = runtime / 'setup_runtime.sh'
    if not setup.exists():
        raise RuntimeError('找不到安装脚本。')
    os.chmod(setup, 0o755)
    env = os.environ.copy()
    env.setdefault('COMMERCIAL_IMAGE_ROUTER_SOURCE', str(repo_root()))
    cmd = ['bash', str(setup), f'--profile={profile}']
    if args.dry_run or env.get('COMMERCIAL_IMAGE_RUNTIME_DRY_RUN') == '1':
        cmd.append('--dry-run')
    if args.no_smoke_test:
        cmd.append('--no-smoke-test')
    if args.skip_model_download:
        cmd.append('--skip-model-download')
    extra = env.get('COMMERCIAL_IMAGE_ROUTER_INSTALL_ARGS', '').split()
    cmd.extend(extra)
    run(cmd, cwd=str(runtime), env=env, quiet=False)
    say('')
    if profile == 'skill-only':
        say('「AI图片制作」Skill 已经安装成功。当前只安装了规则，没有安装本地生图模型。')
    elif profile == 'qwen':
        say('「AI图片制作」Qwen 中文增强能力已经安装成功。')
    else:
        say('「AI图片制作」基础生图能力已经安装成功，可以开始使用了。')
    say('')
    say('接下来你可以直接发给我：')
    say('1. 一句想生成图片的需求；')
    say('2. 一张要处理的图片；')
    say('3. 标题、文案、尺寸或风格要求。')
    say('')
    say('默认主模型是 JuggernautXL，适合高质感主视觉和商业氛围图。')
    say('如果之后要做短中文小红书图、古诗图，或明确要模型自己写中文，我会按需安装 Qwen。')


def main(argv: list[str] | None = None):
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        install(args)
    except Exception as e:
        print('', file=sys.stderr)
        print('「AI图片制作」暂时没有安装成功。', file=sys.stderr)
        print('原因：' + str(e), file=sys.stderr)
        print('你可以把这段失败提示转发给我，我会继续帮你处理。', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
