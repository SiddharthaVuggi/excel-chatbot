from transformers import pipeline

_generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    device="cpu",           
)

def call_llm(prompt: str, max_tokens: int = 256) -> str:
    """
    Generate text with Flan-T5 (CPU). Uses only max_new_tokens
    to avoid duplicate-length warnings.
    """
    resp = _generator(prompt, max_new_tokens=max_tokens)[0]["generated_text"]
    return resp.strip()
