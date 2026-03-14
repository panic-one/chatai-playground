import os
import anthropic
from collections.abc import Iterator

_client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))


def stream_claude(user_message: str, model: str) -> Iterator[str]:
    with _client.messages.stream(
        model=model,
        max_tokens=4096,
        messages=[{"role": "user", "content": user_message}],
    ) as stream:
        for text in stream.text_stream:
            yield text
