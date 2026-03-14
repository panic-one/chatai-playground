from collections.abc import Iterator
from .providers.claude import stream_claude
from .providers.deepseek import stream_deepseek
from .providers.gemini import stream_gemini
from .providers.openai import stream_openai

DEFAULT_MODEL = "gpt-4o-mini"

DEFAULT_PROVIDER_MODEL = {
    "openai": "gpt-4o-mini",
    "gemini": "gemini-2.5-flash",
    "claude": "claude-sonnet-4-6",
    "deepseek": "deepseek-coder",
}

MODEL_MAP = {
    "gpt-4o-mini": stream_openai,
    "gemini-2.5-flash": stream_gemini,
    "claude-sonnet-4-6": stream_claude,
    "deepseek-coder": stream_deepseek,
}

def decided_model(provider: str) -> str:
    model = DEFAULT_PROVIDER_MODEL.get(provider)
    if not model:
        raise ValueError(f"Unsupported provider: {provider}")
    return model

def stream_ai_response(user_message: str, model: str | None = None) -> Iterator[str]:
    if not user_message.strip():
        raise ValueError("user_message is required")
    
    model = model or DEFAULT_MODEL
    
    fn = MODEL_MAP.get(model)
    if not fn:
        raise ValueError(f"Unsupported model: {model}")
    
    return fn(user_message, model)
