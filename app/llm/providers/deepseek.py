import os
from openai import OpenAI
from collections.abc import Iterator


def stream_deepseek(user_message: str, model: str) -> Iterator[str]:
    client = OpenAI(
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
    )
    with client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": user_message}],
        stream=True,
    ) as stream:
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta
