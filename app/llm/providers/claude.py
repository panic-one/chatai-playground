import os
from anthropic import Anthropic
from collections.abc import Iterator

AI_PROMPT = "あなたは親切でわかりやすいAIアシスタントです"

client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

def stream_claude(user_message: str, model: str) -> Iterator[str]:
    with client.message.stream(
        model=model,
        max_tokens=1024,
        system=AI_PROMPT,
        messages=[
            {"role": "user", "content": user_message}
        ]
    ) as stream:
        for text in stream.text_stream:
            if text:
                yield text