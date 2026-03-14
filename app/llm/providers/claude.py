import os
import anthropic
from collections.abc import Iterator


def stream_claude(user_message: str, model: str) -> Iterator[str]:
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    with client.messages.stream(
        model=model,
        max_tokens=4096,
        messages=[{"role": "user", "content": user_message}],
    ) as stream:
        for text in stream.text_stream:
            yield text
