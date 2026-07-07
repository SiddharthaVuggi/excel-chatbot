from transformers import pipeline

_generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    device="cpu", """central processing unit """           
)

def call_llm(prompt: str, max_tokens: int = 256) -> str:
    """
    Generate text with Flan-T5 (CPU). Use only max_new_tokens
    to avoid duplicate-length warnings further.
    """
    resp = _generator(prompt, max_new_tokens=max_tokens)[0]["generated_text"]
    return resp.strip()
