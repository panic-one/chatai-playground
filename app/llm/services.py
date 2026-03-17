from collections.abc import Iterator
from dataclasses import dataclass
from .analyze import request_score, analyze_user_message, AnalysisResult
from .providers.claude import stream_claude
from .providers.deepseek import stream_deepseek
from .providers.gemini import stream_gemini
from .providers.openai import stream_openai

DEFAULT_PROVIDER = "openai"

PROVIDER_CONFIG = {
    "openai": {
        "stream_fn": stream_openai,
        "models": [
            {"name": "gpt-4o-mini", "min_score": 0, "max_score": 49},
            {"name": "gpt-4.1", "min_score": 50, "max_score": 100},
        ],
    },

    "gemini": {
        "stream_fn": stream_gemini,
        "models": [
            {"name": "gemini-2.5-flash-lite", "min_score": 0, "max_score": 24},
            {"name": "gemini-2.5-flash", "min_score": 25, "max_score": 74},
            {"name": "gemini-2.5-pro", "min_score": 75, "max_score": 100}
        ],
    },

    "claude": {
        "stream_fn": stream_claude,
        "models": [
            {"name": "claude-haiku-4-5", "min_score": 0, "max_score": 24},
            {"name": "claude-sonnet-4-6", "min_score": 25, "max_score": 74},
            {"name": "claude-opus-4-6", "min_score": 75, "max_score": 100}
        ],
    },

    "deepseek": {
        "stream_fn": stream_deepseek,
        "models": [
            {"name": "deepseek-chat", "min_score": 0, "max_score": 49},
            {"name": "deepseek-coder", "min_score": 50, "max_score": 100},
        ],
    },
}

@dataclass
class LLMSelection:
    provider: str
    model: str
    score: int
    routing_mode: str

def get_provider_config(provider: str) -> dict:
    config = PROVIDER_CONFIG.get(provider)
    if not config:
        raise ValueError(f"Unsupported provider: {provider}")
    return config

def get_stream_fn(provider: str):
    return get_provider_config(provider)["stream_fn"]

def valid_model_for_provider(provider: str, model: str) -> bool:
    config = get_provider_config(provider)
    return any(m["name"] == model for m in config["models"])

def decide_model(provider: str, score: int) -> str:
    config = get_provider_config(provider)
    for m in config["models"]:
        if m["min_score"] <= score <= m["max_score"]:
            return m["name"]
    raise ValueError(f"No model matched score={score} for provider={provider}")

def resolve_with_provider(provider: str, category: str, difficulty: str) -> LLMSelection:
    score = request_score(provider, category, difficulty)
    model = decide_model(provider, score)
    return LLMSelection(
        provider=provider,
        model=model,
        score=score,
        routing_mode="provider_auto_model",
    )

def resolve_auto_provider(category: str, difficulty: str) -> LLMSelection:
    candidates = []

    for provider in PROVIDER_CONFIG.keys():
        score = request_score(provider, category, difficulty)
        model = decide_model(provider, score)
        candidates.append(
            LLMSelection(
                provider=provider,
                model=model,
                score=score,
                routing_mode="full_auto",
            )
        )
    return max(candidates, key=lambda x: x.score)

def stream_ai_response(user_message: str, provider: str | None = None, model: str | None = None) -> Iterator[str]:
    if not user_message.strip():
        raise ValueError("user_message is required")
    
    analysis = analyze_user_message(user_message)

    if model:
        selected_provider = provider or DEFAULT_PROVIDER
        if not valid_model_for_provider(selected_provider, model):
            raise ValueError(f"Model '{model}' is not supported for provider '{selected_provider}'")
        fn = get_stream_fn(selected_provider)
        return fn(user_message, model)
    
    if provider and provider != "auto":
        selection = resolve_with_provider(
            provider=provider,
            category=analysis.category,
            difficulty=analysis.difficulty,
        )
    else:
        selection = resolve_auto_provider(
            category=analysis.category,
            difficulty=analysis.difficulty,
        )

    fn = get_stream_fn(selection.provider)
    return fn(user_message, selection.model)

def stream_ai_response_with_meta(user_message: str, provider: str | None = None, model: str | None = None,) -> tuple[Iterator[str], LLMSelection, AnalysisResult]:
    if not user_message.strip():
        raise ValueError("user_message is required")
    
    analysis = analyze_user_message(user_message)

    if model:
        selected_provider = provider or DEFAULT_PROVIDER
        if not valid_model_for_provider(selected_provider, model):
            raise ValueError(f"Model '{model}' is not supported for provider '{selected_provider}'")
        
        selection = LLMSelection(
            provider=selected_provider,
            model=model,
            score=-1,
            routing_mode="manual_model"
        )
        fn = get_stream_fn(selected_provider)
        return fn(user_message, model), selection, analysis
    
    if provider and provider != "auto":
        selection = resolve_with_provider(
            provider=provider,
            category=analysis.category,
            difficulty=analysis.difficulty,
        )
    else:
        selection = resolve_auto_provider(
            category=analysis.category,
            difficulty=analysis.difficulty,
        )
    
    fn = get_stream_fn(selection.provider)
    stream = fn(user_message, selection.model)
    return stream, selection, analysis

