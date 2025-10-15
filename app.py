# app.py
import os
import logging
from deep_translator import GoogleTranslator as Translator
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# ------------------------------
# Logging
# ------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------------------------
# Model Setup (Lazy Load)
# ------------------------------
MODEL_NAME = "distilgpt2"  # Small, fast model for testing
pipe = None  # lazy init

def get_pipeline():
    """Load model only once per container (lazy init)."""
    global pipe
    if pipe is None:
        logger.info(f"🚀 Loading {MODEL_NAME} model for the first time...")

        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device=0 if os.environ.get("CUDA_VISIBLE_DEVICES") else -1,
        )
        logger.info("✅ Model loaded successfully.")
    return pipe

translator = Translator()

# ------------------------------
# Tone Instructions
# ------------------------------
TONE_INSTRUCTIONS = {
    "default": "Write in a clear and appetizing restaurant style.",
    "premium": "Write in a premium, high-end tone, highlighting exclusivity and top quality.",
}

# ------------------------------
# Words to Avoid
# ------------------------------
FLUFF_WORDS = ["enjoy", "try", "savor", "delight", "experience"]

# ------------------------------
# Main Function
# ------------------------------
def generate_description(original: str, tone: str = "premium", language: str = "en") -> str:
    """Generate a restaurant-style menu description."""
    prompt = f"""
You are a restaurant branding expert. Rewrite the following text into a polished, appetizing menu description.

Original: {original}

Rules:
1. Write in {TONE_INSTRUCTIONS.get(tone, TONE_INSTRUCTIONS['default'])}
2. Preserve all brand names and quantities exactly as given.
3. Keep quantities in digit form (e.g., 12 wings, 2 strips).
4. Limit the description to a maximum of 3 concise sentences.
5. Do not use these words: {", ".join(FLUFF_WORDS)}.
6. Output only the final menu description with no extra commentary.

Enhanced description:
"""

    try:
        pipe = get_pipeline()
        outputs = pipe(prompt, max_new_tokens=100, temperature=0.7, top_p=0.9)
        result = outputs[0]["generated_text"]

        if language.lower() != "en":
            result = translator.translate(result, source="en", target=language)

        return result.strip()

    except Exception as e:
        logger.error(f"❌ Error generating description: {e}", exc_info=True)
        return f"[Error: {e}]"
