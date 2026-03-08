import os
from openai import OpenAI
from collections.abc import Iterator

AI_PROMPT = "あなたは親切でわかりやすいAIアシスタントです"

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

def stream_ai_response(user_message: str, model: str | None = None) -> Iterator[str]:
    if not user_message or not user_message.strip():
        raise ValueError("user_message is required")
    
    model_name = model or os.environ.get("DEFAULT_LLM_MODEL", "gpt-4o-mini")

    stream = client.chat.completions.create(
        model=model_name,
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