from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch
from django.core.cache import cache

MODEL_PHI = 'microsoft/Phi-3-mini-128k-instruct'
model_id = "meta-llama/Meta-Llama-3-8B"


def load_model():
    # Check if the model is already in cache
    generator = cache.get('generator')
    if not generator:
        try:
            model = AutoModelForCausalLM.from_pretrained(
                "microsoft/Phi-3-mini-128k-instruct", device_map="cpu", torch_dtype="auto", trust_remote_code=True)
            tokenizer = AutoTokenizer.from_pretrained(
                "microsoft/Phi-3-mini-128k-instruct")
            generator = pipeline(
                "text-generation", model=model, tokenizer=tokenizer)

            # Save the generator to cache
            cache.set('generator', generator, timeout=None)
        except Exception as e:
            print(f"Error loading model: {e}")
            return None
    return generator
