# =====================================
# 🧠 Base Image — Python + CUDA Ready for Torch
# =====================================
FROM nvidia/cuda:12.1.1-base-ubuntu22.04

# =====================================
# 🧩 System Setup
# =====================================
ENV DEBIAN_FRONTEND=noninteractive
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
# ⚡ Preload DistilGPT2 model to avoid cold start
# =====================================
RUN python3 - <<EOF
from transformers import AutoModelForCausalLM, AutoTokenizer
model = "distilgpt2"
print("📦 Downloading model and tokenizer...")
AutoTokenizer.from_pretrained(model)
AutoModelForCausalLM.from_pretrained(model)
print("✅ Model downloaded successfully!")
EOF

# =====================================
# 🌐 Expose Healthcheck Port
# =====================================
EXPOSE 8080

# =====================================
# 🚀 Start RunPod Handler
# =====================================
CMD ["python3", "runpod_handler.py"]
