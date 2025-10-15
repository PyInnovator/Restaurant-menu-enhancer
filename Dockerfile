# =====================================
# 🧠 Base Image — lightweight Python + CUDA (optional)
# =====================================
FROM python:3.11-slim

# =====================================
# 🧩 System Setup
# =====================================
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git wget curl vim \
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
# 🌐 Expose Healthcheck Port
# =====================================
EXPOSE 8080

# =====================================
# 🚀 Start RunPod Serverless Handler
# =====================================
CMD ["python3", "runpod_handler.py"]
