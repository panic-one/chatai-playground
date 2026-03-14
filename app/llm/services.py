from collections.abc import Iterator
from .providers.claude import stream_claude
from .providers.deepseek import stream_deepseek
from .providers.gemini import stream_gemini
from .providers.openai import stream_openai

DEFAULT_MODEL = "gpt-4o-mini"

PROVIDER_CONFIG = {
    "openai": ("gpt-4o-mini", stream_openai),
    "gemini": ("gemini-2.5-flash", stream_gemini),
    "claude": ("claude-sonnet-4-6", stream_claude),
    "deepseek": ("deepseek-coder", stream_deepseek),
}

DEFAULT_PROVIDER_MODEL = {
    provider: config[0] for provider, config in PROVIDER_CONFIG.items()
}

MODEL_MAP = {
    config[0]: config[1] for config in PROVIDER_CONFIG.values()
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
