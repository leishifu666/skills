#!/bin/sh
# LSF Lemo-Opuscar：定位或获取风格资料库，并输出资料库路径。
# 用法：
#   sh setup.sh              检查资料库；首次运行时克隆，之后尝试更新；最后输出 LIB=<path>
#   sh setup.sh deps         同时安装 Node.js、Python 包和无头浏览器
#   sh setup.sh demo <slug>  下载某种风格的示例源代码（仅供参考）
# 资料库是 github.com/lemomo-ai/lemo-opuscar 的稀疏克隆，包含指南、core/ 工具和全部 STYLE.md（约 60 MB）。
# 示例源代码按需下载；大型资源通过 tools/fetch.sh 获取。
set -e
REPO=https://github.com/lemomo-ai/lemo-opuscar.git

# 1. 选择资料库：LEMO_OPUSCAR_HOME、当前所在的资料库克隆版、当前工作区中的现有克隆版、工作区内的新目录。
is_lib() { [ -f "$1/AGENTS.md" ] && [ -d "$1/core/render" ]; }
if [ -n "$LEMO_OPUSCAR_HOME" ]; then LIB=$LEMO_OPUSCAR_HOME
elif top=$(git rev-parse --show-toplevel 2>/dev/null) && is_lib "$top"; then LIB=$top
elif is_lib "$PWD/work/lemo-opuscar"; then LIB="$PWD/work/lemo-opuscar"
else LIB="$PWD/work/lemo-opuscar-library"
fi
case "$LIB" in /*) ;; *) LIB=$(pwd)/$LIB ;; esac

if [ "$(git -C "$LIB" config --get lemo.managed 2>/dev/null)" = true ]; then
  # 这是脚本自行管理的克隆版：若干净则更新，不覆盖本地改动。
  if [ -n "$(git -C "$LIB" status --porcelain --untracked-files=no 2>/dev/null)" ]; then
    echo "! $LIB 有本地改动，未更新"
  else
    git -C "$LIB" pull --quiet --ff-only 2>/dev/null || echo "! 无法更新 $LIB（可能离线）；继续使用本地副本"
  fi
elif ! is_lib "$LIB"; then
  [ -e "$LIB" ] && [ -n "$(ls -A "$LIB" 2>/dev/null)" ] && { echo "✗ $LIB 已存在但不是 Lemo-Opuscar 资料库。请将 LEMO_OPUSCAR_HOME 设置为其他目录。"; exit 1; }
  command -v git >/dev/null || { echo "✗ 下载资料库需要 git"; exit 1; }
  mkdir -p "$(dirname "$LIB")"
  echo "↓ 正在将风格资料库下载到 $LIB"
  git clone --quiet --depth 1 --filter=blob:none --sparse "$REPO" "$LIB" || { rm -rf "$LIB"; echo "✗ 下载失败（可能离线）"; exit 1; }
  # git 版本低于 2.35 时不支持 --no-cone，退回完整检出。
  git -C "$LIB" sparse-checkout set --no-cone '/*' '!/styles/*/demo/' '!/styleboard/' 2>/dev/null \
    || git -C "$LIB" sparse-checkout disable
  git -C "$LIB" config lemo.managed true
fi
LIB=$(cd "$LIB" && pwd -P)

node_ok() { [ -f "$LIB/node_modules/.lemo-ok" ]; }
py_ok() { [ -f "$LIB/.venv/.lemo-ok" ]; }

case "$1" in
  deps)
    cd "$LIB"
    if ! node_ok; then
      npm install --no-audit --no-fund --silent
      node node_modules/playwright-core/cli.js install chromium-headless-shell   # 渲染器使用的浏览器
      touch node_modules/.lemo-ok
    fi
    if ! py_ok; then
      if command -v uv >/dev/null; then uv venv --quiet --allow-existing --python 3.12 && uv pip install --quiet -r requirements.txt
      else
        python3 -c 'import sys; sys.exit(sys.version_info < (3, 11))' || { echo "✗ 需要 Python 3.11+，或安装可下载对应版本的 uv"; exit 1; }
        python3 -m venv .venv && .venv/bin/pip install --quiet -r requirements.txt
      fi
      touch .venv/.lemo-ok
    fi
    ;;
  demo)
    [ -n "$2" ] && [ -f "$LIB/styles/$2/STYLE.md" ] || { echo "用法：sh setup.sh demo <slug>（slug 列表见 $LIB/styles/README.md）"; exit 1; }
    if git -C "$LIB" sparse-checkout list >/dev/null 2>&1 && [ ! -d "$LIB/styles/$2/demo" ]; then
      git -C "$LIB" sparse-checkout add "/styles/$2/demo/"
    fi
    echo "示例源代码：$LIB/styles/$2/demo"
    ;;
esac

# 2. 只检查渲染所需系统工具，不自动安装。
miss=""
if command -v node >/dev/null; then
  [ "$(node -p 'process.versions.node.split(".")[0]')" -ge 20 ] || miss="$miss Node 20+（当前为 $(node -v)）"
else miss="$miss Node 20+"; fi
command -v ffmpeg >/dev/null || miss="$miss ffmpeg"
command -v uv >/dev/null || python3 -c 'import sys; sys.exit(sys.version_info < (3, 11))' 2>/dev/null || miss="$miss Python 3.11+（或 uv）"
[ -n "$miss" ] && echo "! 缺少：$miss"
node_ok && py_ok || echo "! 尚未安装 Python/Node 依赖：首次渲染前运行 sh setup.sh deps（需要几分钟）"
echo "LIB=$LIB"
