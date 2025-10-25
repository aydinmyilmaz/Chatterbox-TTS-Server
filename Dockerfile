# ---------------------------------------------------------------------------
# 🧠 Chatterbox Multilingual TTS — RunPod Serverless Optimized Dockerfile
# ---------------------------------------------------------------------------
# • CUDA 12.4 + PyTorch 2.6 base
# • Builds quickly and caches pip layers efficiently
# • Includes multilingual Chatterbox model
# • Handler-based entrypoint for RunPod Serverless
# ---------------------------------------------------------------------------

FROM pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime

# --- System dependencies ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    git ffmpeg libsndfile1 build-essential python3-venv && \
    rm -rf /var/lib/apt/lists/*

# --- Working directory ---
WORKDIR /workspace

# --- Copy dependency lists first (for layer caching) ---
COPY requirements.txt .

# --- Create venv and install deps in correct order ---
RUN python3 -m venv /workspace/venv && \
    . /workspace/venv/bin/activate && \
    pip install --upgrade pip setuptools wheel && \
    # Preinstall core libs that pkuseg needs
    pip install numpy==1.26.4 cython && \
    # Install pkuseg first with isolation disabled
    pip install pkuseg==0.0.25 --no-build-isolation && \
    # Then the rest (split for cache efficiency)
    pip install -r requirements.txt && \
    # Optional: clean pip cache to save space
    rm -rf ~/.cache/pip

# --- Copy rest of project ---
COPY . .

# --- Ensure multilingual config exists ---
RUN echo -e "\nmodel:\n  repo_id: ResembleAI/chatterbox-multilingual" > /workspace/config.yaml

# --- Entrypoint for RunPod Serverless ---
CMD ["/workspace/venv/bin/python", "handler.py"]
