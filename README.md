# Menu Enhancer (Local Model)

This project runs a Flask API that loads a local LLM model (e.g., DeepSeek-V3.1) inside the container.

## Files
- `app.py` : Flask API that loads the model and exposes `/enhance`
- `requirements.txt` : Python dependencies
- `Dockerfile` : Example GPU Dockerfile (uses CUDA base image)

## Deploy to RunPod Serverless (summary)
1. Zip this folder and upload it to RunPod Serverless as a custom container source.
2. Choose a GPU resource (A100/H100 recommended for large models).
3. If needed, edit the Dockerfile to install the correct torch wheel for the selected CUDA version.
4. Add environment variable `MODEL_NAME` if you want to load a different model.
5. Deploy and wait for the build logs to finish. Use the `/enhance` endpoint to send POST requests.
