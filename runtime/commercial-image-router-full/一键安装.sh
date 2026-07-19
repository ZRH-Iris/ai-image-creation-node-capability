#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

echo "========================================"
echo " 图片处理能力安装包"
echo "========================================"
echo ""
echo "这个安装会自动配置："
echo "- 图片生成能力"
echo "- 商品图/海报能力"
echo "- 中文字体和排版能力"
echo "- 抠图和高清放大能力"
echo ""
echo "安装过程会下载较大的模型文件，可能需要较长时间。"
echo "请保持网络连接，不要关闭窗口。"
echo ""
read -r -p "按回车开始安装，或按 Ctrl+C 取消... " _

bash setup_runtime.sh

echo ""
echo "========================================"
echo " 安装完成"
echo "========================================"
echo ""
echo "接下来打开 Hermes/Harness，输入："
echo ""
echo "  /reload-skills"
echo "  /skill commercial-image-router"
echo ""
echo "然后就可以直接让它生成、修改、放大、处理图片。"
echo ""
