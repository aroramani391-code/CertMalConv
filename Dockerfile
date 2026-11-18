# CUDA 12.1 base image matched to the training environment reported in the paper.
FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04

LABEL org.opencontainers.image.title="CertMalConv" \
      org.opencontainers.image.description="Certifiably robust multi-modal malware detection" \
      org.opencontainers.image.source="https://github.com/certmalconv/certmalconv" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.version="0.3.2"

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# --- System dependencies ----------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        git \
        git-lfs \
        curl \
        wget \
        ca-certificates \
        libcapstone-dev \
        libssl-dev \
        libffi-dev \
        libjpeg-dev \
        libpng-dev \
        pkg-config \
        python3.11 \
        python3.11-dev \
        python3.11-venv \
        python3-pip \
    && rm -rf /var/lib/apt/lists/* \
    && git lfs install

RUN ln -sf /usr/bin/python3.11 /usr/local/bin/python \
    && ln -sf /usr/bin/python3.11 /usr/local/bin/python3

# --- Python dependencies ----------------------------------------------------
WORKDIR /workspace/certmalconv

COPY requirements.txt pyproject.toml ./
RUN pip install --upgrade pip==24.0 \
    && pip install --index-url https://download.pytorch.org/whl/cu121 \
        torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 \
    && pip install -r requirements.txt

# --- Source code ------------------------------------------------------------
COPY . .
RUN pip install -e ".[dev]"

# --- Non-root user ----------------------------------------------------------
RUN groupadd -r certmalconv && useradd -r -g certmalconv -d /workspace certmalconv \
    && chown -R certmalconv:certmalconv /workspace
USER certmalconv

# --- Healthcheck ------------------------------------------------------------
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import certmalconv, torch; assert torch.cuda.is_available()" || exit 1

CMD ["bash"]
