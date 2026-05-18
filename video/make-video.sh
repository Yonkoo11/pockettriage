#!/usr/bin/env zsh
# One command to build the full demo video
# Usage: zsh video/make-video.sh [site-url]

set -e
SCRIPT_DIR="${0:a:h}"

echo "=== Agent Colosseum Demo Video ==="
echo ""

echo "[1/4] Capturing frames..."
node "$SCRIPT_DIR/capture-frames.js" "${1:-https://yonkoo11.github.io/agent-colosseum/}"

echo ""
echo "[2/4] Generating audio..."
zsh "$SCRIPT_DIR/generate-audio.sh"

echo ""
echo "[3/4] Compositing captions..."
python3 "$SCRIPT_DIR/generate-captions.py"

echo ""
echo "[4/4] Assembling video..."
zsh "$SCRIPT_DIR/assemble.sh"

echo ""
echo "=== Complete ==="
