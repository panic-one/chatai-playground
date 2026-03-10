import os
from collections.abc import Iterator
from .providers import(
    stream_claude,
    stream_deepseek,
    stream_gemini,
    stream_openai
)

def stream_ai_response(user_message: str, provider: str, model: str | None = None) -> Iterator[str]:
    if not user_message.strip():
        raise ValueError("user_message is required")
    
    if provider == "openai":
        model = model or os.getenv("OPENAI_MODEL")
        return stream_openai(user_message, model)
    elif provider == "gemini":
        model = model or os.getenv("GEMINI_MODEL")
        return stream_gemini(user_message, model)
    elif provider == "claude":
        model = model or os.getenv("CLAUDE_MODEL")
        return stream_claude(user_message, model)
    elif provider == "deepseek":
        model = model or os.getenv("DEEPSEEK_MODEL")
        return stream_deepseek(user_message, model)
    else:
        raise ValueError(f"Unsupported provider: {provider}")