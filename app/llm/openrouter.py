import os
from collections.abc import Iterator
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def stream_openrouter(user_message: str, model: str) -> Iterator[str]:
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

    for chunk in response:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta