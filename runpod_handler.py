# runpod_handler.py
import runpod
import logging
from datetime import datetime
from app import generate_description
from flask import Flask, jsonify
import threading

# ==========================================================
# 🧾 Logging Configuration
# ==========================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("runpod_handler")

# ==========================================================
# 💓 Flask Healthcheck Server (Runs in Background)
# ==========================================================
health_app = Flask(__name__)

@health_app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "DeepSeek model ready!"})

def start_health_server():
    """Starts healthcheck server on port 8080 in a background thread."""
    health_app.run(host="0.0.0.0", port=8080, debug=False, use_reloader=False)

# Start healthcheck server in a separate thread
threading.Thread(target=start_health_server, daemon=True).start()

# ==========================================================
# 🚀 RunPod Handler Function
# ==========================================================
def handler(event):
    try:
        logger.info("📩 New request received")

        # Extract input data safely
        data = event.get("input", {}) or {}
        original = data.get("input") or data.get("text", "")
        tone = data.get("tone", "premium")
        language = data.get("language", "en")

        if not original:
            logger.warning("⚠️ Missing 'input' or 'text' field in request.")
            return {"error": "Missing 'input' or 'text' field in request."}

        logger.info(f"🧠 Processing input: {original[:80]}...")
        logger.info(f"🎨 Tone: {tone} | 🌐 Language: {language}")

        # Generate description
        result = generate_description(original, tone, language)

        logger.info("✅ Successfully generated enhanced description.")
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "input_text": original,
            "enhanced_description": result,
        }

    except Exception as e:
        logger.error(f"❌ Error in handler: {e}", exc_info=True)
        return {"error": str(e)}

# ==========================================================
# 🏁 Entry Point — RunPod Serverless
# ==========================================================
if __name__ == "__main__":
    logger.info("🚀 Starting RunPod handler + healthcheck server...")
    runpod.serverless.start({"handler": handler})
