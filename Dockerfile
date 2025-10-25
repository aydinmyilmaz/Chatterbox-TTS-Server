# --- Base Image (CUDA + PyTorch) ---
FROM pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime

# --- System packages ---
RUN apt-get update && apt-get install -y \
    git ffmpeg libsndfile1 build-essential python3.10-venv \
    && rm -rf /var/lib/apt/lists/*

# --- Workspace setup ---
WORKDIR /workspace
COPY . .

# --- Python setup ---
RUN python3 -m venv /workspace/venv && \
    . /workspace/venv/bin/activate && \
    pip install --upgrade pip setuptools wheel && \
    pip install numpy==1.26.4 cython && \
    pip install pkuseg==0.0.25 --no-build-isolation && \
    pip install chatterbox-tts fastapi uvicorn librosa pydub watchdog python-multipart tqdm safetensors soundfile \
    git+https://github.com/resemble-ai/Resemblyzer.git \
    openai-whisper hf_transfer

# --- Force multilingual model ---
RUN echo -e "\nmodel:\n  repo_id: ResembleAI/chatterbox-multilingual" > /workspace/config.yaml

# --- Copy handler script ---
COPY handler.py /workspace/handler.py

# --- Start Serverless Entry ---
CMD ["python", "handler.py"]
