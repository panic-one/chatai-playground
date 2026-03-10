import os
from anthropic import Anthropic
from collections.abc import Iterator

AI_PROMPT = "あなたは親切でわかりやすいAIアシスタントです"

client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

def stream_claude(user_message: str, model: str) -> Iterator[str]:
    stream = client.messages.stream(
        model=model,
        max_tokens=1024,
        system=AI_PROMPT,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    for chunk in stream:
        if chunk.type == "content_block_delta":
            text = chunk.delta.text
            if text:
                yield text