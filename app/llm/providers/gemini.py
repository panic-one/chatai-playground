import os
import google.generativeai as genai
from collections.abc import Iterator

AI_PROMPT = "あなたは親切でわかりやすいAIアシスタントです"

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def stream_gemini(user_message: str, model: str) -> Iterator[str]:
    model = genai.GenerativeModel(model)
    response = model.generate_content(
        f"{AI_PROMPT}\n{user_message}",
        stream=True
    )

    for chunk in response:
        if chunk.text:
            yield chunk.text