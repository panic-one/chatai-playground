import os
from openai import OpenAI
from collections.abc import Iterator

AI_PROMPT = "あなたは親切でわかりやすいAIアシスタントです"

client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY")
)

def stream_openai(user_message: str, model: str) -> Iterator[str]:
    stream = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": AI_PROMPT},
            {"role": "user", "content": user_message},
        ],
        stream=True
    )

    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta