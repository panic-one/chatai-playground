import os
from openai import OpenAI
from collections.abc import Iterator

_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))


def stream_openai(user_message: str, model: str) -> Iterator[str]:
    response = _client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": user_message}],
        stream=True,
    )
    for chunk in response:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta
