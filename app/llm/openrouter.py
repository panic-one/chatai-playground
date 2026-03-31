import os
from collections.abc import Iterator
from openai import OpenAI
from dataclasses import dataclass

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

@dataclass
class OpenRouterChunk:
    content: str
    actual_model: str | None = None
    actual_provider: str | None = None

def stream_openrouter(user_message: str, model: str) -> Iterator[OpenRouterChunk]:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": user_message},
        ],
        stream=True,
        extra_headers={
            "HTTP-Referer": "http://127.0.0.1:5000",
            "X-OpenRouter-Title": "chatai-playground",
        },
    )

    actual_model = None
    actual_provider = None

    for chunk in response:
        if actual_model is None and getattr(chunk, "model", None):
            actual_model = chunk.model
            actual_provider = actual_model.split("/")[0] if "/" in actual_model else actual_model

        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta.content
        if delta:
            yield OpenRouterChunk(
                content=delta,
                actual_model=actual_model,
                actual_provider=actual_provider,
            )