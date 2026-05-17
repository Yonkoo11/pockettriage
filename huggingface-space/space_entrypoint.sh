#!/usr/bin/env bash
set -euo pipefail

# Start Ollama in the background
ollama serve > /tmp/ollama.log 2>&1 &
OLLAMA_PID=$!

# Wait for Ollama HTTP to come up
for i in {1..60}; do
  if curl -fsS http://127.0.0.1:11434/ >/dev/null 2>&1; then
    echo "ollama: up after ${i}s"
    break
  fi
  sleep 1
done

# Pull the model. First boot is slow (~7 GB); subsequent boots reuse cached blobs.
if ! ollama list | awk '{print $1}' | grep -qx "${POCKETTRIAGE_OLLAMA_TAG}"; then
  echo "ollama: pulling ${POCKETTRIAGE_OLLAMA_TAG} (first boot, ~7 GB)…"
  ollama pull "${POCKETTRIAGE_OLLAMA_TAG}"
fi

# Sanity ping (warm up model)
curl -fsS http://127.0.0.1:11434/api/chat \
  -d "{\"model\":\"${POCKETTRIAGE_OLLAMA_TAG}\",\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}],\"stream\":false,\"options\":{\"num_predict\":4}}" \
  > /dev/null || echo "warmup: failed (model may still be loading; UI will retry)"

# Launch the Gradio app
cd /home/user/app/laptop
exec python app.py
