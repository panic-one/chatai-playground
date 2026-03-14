import os
from openai import OpenAI
from collections.abc import Iterator


def stream_openai(user_message: str, model: str) -> Iterator[str]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    with client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": user_message}],
        stream=True,
    ) as stream:
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta
