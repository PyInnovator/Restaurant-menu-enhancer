# =====================================
# 🧠 Base Image — lightweight Python + CUDA
# =====================================
FROM nvidia/cuda:12.1.1-base-ubuntu22.04

# =====================================
# 🧩 System Setup
# =====================================
ENV DEBIAN_FRONTEND=noninteractive
ENV TRANSFORMERS_CACHE=/root/.cache/huggingface
ENV HF_HOME=/root/.cache/huggingface

RUN apt-get update && apt-get install -y \
    python3 python3-pip git wget curl vim \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# =====================================
# 🧱 Copy Project Files
# =====================================
COPY . /app

# =====================================
# 🧰 Install Dependencies
# =====================================
RUN pip install --no-cache-dir -r requirements.txt

# =====================================
# ⚡ Pre-Download Model (optional, no token hardcoded)
# =====================================
# At runtime, HF_TOKEN will be passed; we can skip pre-download in Dockerfile
# Or, use build arg if necessary (HF_TOKEN passed from host)
ARG HF_TOKEN
RUN if [ -n "$HF_TOKEN" ]; then \
        python3 -c "from transformers import AutoTokenizer, AutoModelForCausalLM; \
        AutoTokenizer.from_pretrained('deepseek-ai/DeepSeek-V3.1', use_auth_token='$HF_TOKEN'); \
        AutoModelForCausalLM.from_pretrained('deepseek-ai/DeepSeek-V3.1', use_auth_token='$HF_TOKEN')" \
    ; fi

# =====================================
# 🌐 Expose Healthcheck Port
# =====================================
EXPOSE 8080

# =====================================
# 🚀 Start RunPod Serverless Handler
# =====================================
CMD ["python3", "runpod_handler.py"]
