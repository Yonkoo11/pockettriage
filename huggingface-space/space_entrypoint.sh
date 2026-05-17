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

# Warm up the model with a real-shaped JSON call so weights are paged in
# and the first user request doesn't pay the 30-second load cost.
echo "warmup: generating short JSON to load weights…"
curl -fsS --max-time 600 http://127.0.0.1:11434/api/chat \
  -d "{
    \"model\":\"${POCKETTRIAGE_OLLAMA_TAG}\",
    \"keep_alive\":\"${POCKETTRIAGE_OLLAMA_KEEP_ALIVE}\",
    \"messages\":[{\"role\":\"user\",\"content\":\"Reply with only the JSON object {\\\"ok\\\":true} and nothing else.\"}],
    \"stream\":false,
    \"options\":{\"num_predict\":24,\"temperature\":0.0}
  }" > /tmp/warmup.json 2>&1 && echo "warmup ok" || echo "warmup: failed (UI will still try)"

# Launch the Gradio app
cd /home/user/app/laptop
exec python app.py
