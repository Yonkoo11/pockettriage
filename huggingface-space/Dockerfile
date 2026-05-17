FROM python:3.12-slim

# System deps. Ollama's installer requires zstd to extract its bundle.
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates zstd \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama (native binary)
RUN curl -fsSL https://ollama.com/install.sh | sh

# Non-root user for HF Spaces
RUN useradd -m -u 1000 user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    OLLAMA_HOST=127.0.0.1:11434 \
    OLLAMA_KEEP_ALIVE=24h \
    POCKETTRIAGE_BACKEND=ollama \
    POCKETTRIAGE_OLLAMA_TAG=gemma4:e2b \
    POCKETTRIAGE_OLLAMA_TIMEOUT_S=480 \
    POCKETTRIAGE_OLLAMA_KEEP_ALIVE=24h \
    POCKETTRIAGE_OLLAMA_NUM_PREDICT=200 \
    GRADIO_SERVER_NAME=0.0.0.0 \
    GRADIO_SERVER_PORT=7860 \
    GRADIO_ANALYTICS_ENABLED=False

USER user
WORKDIR /home/user/app

# Python deps
COPY --chown=user:user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# App source — copied from repo root by Spaces sync
COPY --chown=user:user laptop/ ./laptop/
COPY --chown=user:user who-imci/ ./who-imci/
COPY --chown=user:user space_entrypoint.sh ./space_entrypoint.sh
RUN chmod +x ./space_entrypoint.sh

EXPOSE 7860

CMD ["./space_entrypoint.sh"]
