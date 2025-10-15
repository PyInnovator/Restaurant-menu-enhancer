import os
import logging
import torch
from deep_translator import GoogleTranslator as Translator
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# ------------------------------
# Logging Setup
# ------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MenuEnhancer")

# ------------------------------
# Model Configuration
# ------------------------------
MODEL_NAME = "distilgpt2"  # Small, lightweight model for testing
pipe = None  # Lazy-loaded pipeline instance

def get_pipeline():
    """Load the model once per container (lazy init)."""
    global pipe
    if pipe is None:
        logger.info(f"🚀 Loading model: {MODEL_NAME}")

        try:
            tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

            device = 0 if torch.cuda.is_available() else -1
            logger.info(f"Using device: {'GPU' if device == 0 else 'CPU'}")

            pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                device=device
            )

            logger.info("✅ Model loaded successfully.")
        except Exception as e:
            logger.error(f"❌ Error loading model: {e}", exc_info=True)
            raise e

    return pipe

translator = Translator()

# ------------------------------
# Tone Instructions
# ------------------------------
TONE_INSTRUCTIONS = {
    "default": "Write in a clear, simple, and appetizing restaurant style.",
    "premium": "Write in a premium, elegant tone that highlights quality and sophistication.",
}

# ------------------------------
# Words to Avoid
# ------------------------------
FLUFF_WORDS = ["enjoy", "try", "savor", "delight", "experience"]

# ------------------------------
# Main Description Generator
# ------------------------------
def generate_description(original: str, tone: str = "premium", language: str = "en") -> str:
    """Generate a restaurant-style menu description."""
    prompt = f"""
You are a restaurant branding expert. Rewrite the following into a concise, appealing menu description.

Original: {original}

Rules:
1. Write in {TONE_INSTRUCTIONS.get(tone, TONE_INSTRUCTIONS['default'])}
2. Preserve all brand names and quantities exactly as given.
3. Keep numbers in digit form (e.g., 12 wings, 2 strips).
4. Limit to 2–3 sentences maximum.
5. Do not use: {", ".join(FLUFF_WORDS)}.
6. Return only the rewritten text.

Enhanced description:
"""

    try:
        pipe = get_pipeline()
        outputs = pipe(
            prompt,
            max_new_tokens=80,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )
        result = outputs[0]["generated_text"].split("Enhanced description:")[-1].strip()

        if language.lower() != "en":
            result = translator.translate(result, source="en", target=language)

        return result
    except Exception as e:
        logger.error(f"❌ Error generating description: {e}", exc_info=True)
        return f"[Error: {str(e)}]"
