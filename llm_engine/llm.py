from functools import lru_cache
from transformers import pipeline
import torch


@lru_cache(maxsize=1)
def load_model():
    """
    Load the FLAN-T5 model only once.

    Automatically uses GPU if available,
    otherwise falls back to CPU.
    """

    device = 0 if torch.cuda.is_available() else -1

    return pipeline(
        task="text2text-generation",
        model="google/flan-t5-base",
        tokenizer="google/flan-t5-base",
        device=device,
    )


def call_llm(
    prompt: str,
    max_new_tokens: int = 256,
    temperature: float = 0.7,
    do_sample: bool = False,
) -> str:
    """
    Generate a response using Google's FLAN-T5.

    Args:
        prompt: Input prompt.
        max_new_tokens: Maximum number of generated tokens.
        temperature: Controls randomness.
        do_sample: Enables sampling for more creative responses.

    Returns:
        Generated text.
    """

    if not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    generator = load_model()

    try:
        response = generator(
            prompt,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            do_sample=do_sample,
            truncation=True,
        )

        return response[0]["generated_text"].strip()

    except Exception as e:
        return f"LLM Error: {str(e)}"


if __name__ == "__main__":
    question = "Explain diabetes in simple words."

    answer = call_llm(question)

    print("\nPrompt:")
    print(question)

    print("\nResponse:")
    print(answer)
