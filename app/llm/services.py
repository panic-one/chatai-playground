from collections.abc import Iterator
from dataclasses import dataclass
from .analyze import request_score, analyze_user_message, AnalysisResult
from .openrouter import stream_openrouter


PROVIDER_CONFIG = {
    "openai": [
        {"name": "openai/gpt-4o-mini", "min_score": 0, "max_score": 49},
        {"name": "openai/gpt-4.1", "min_score": 50, "max_score": 100},
    ],

    "gemini": [
            {"name": "google/gemini-2.5-flash-lite", "min_score": 0, "max_score": 24},
            {"name": "google/gemini-2.5-flash", "min_score": 25, "max_score": 74},
            {"name": "google/gemini-2.5-pro", "min_score": 75, "max_score": 100}
        ],

    "claude": [
            {"name": "anthropic/claude-haiku-4-5", "min_score": 0, "max_score": 24},
            {"name": "anthropic/claude-sonnet-4-6", "min_score": 25, "max_score": 74},
            {"name": "anthropic/claude-opus-4-6", "min_score": 75, "max_score": 100}
        ],

    "deepseek": [
            {"name": "deepseek/deepseek-chat", "min_score": 0, "max_score": 49},
            {"name": "deepseek/deepseek-coder", "min_score": 50, "max_score": 100},
        ],
}

@dataclass
class LLMSelection:
    provider: str
    model: str
    score: int
    routing_mode: str

def get_providers(provider: str | None) -> list[str]:
    if not provider or provider == "auto":
        return list(PROVIDER_CONFIG.keys())
    
    if provider not in PROVIDER_CONFIG:
        raise ValueError(f"Unsupported provider: {provider}")
    
    return [provider]

def decide_model(provider: str, score: int) -> str:
    for m in PROVIDER_CONFIG[provider]:
        if m["min_score"] <= score <= m["max_score"]:
            return m["name"]
        
    raise ValueError(f"No model matched score={score} for provider={provider}")

def resolve_selection(category: str, difficulty: str, provider: str | None = None) -> LLMSelection:
    allowed_providers = get_providers(provider)
    candidates: list[LLMSelection] = []

    for p in allowed_providers:
        score = request_score(p, category, difficulty)
        model = decide_model(p, score)
        candidates.append(
            LLMSelection(
                provider=p,
                model=model,
                score=score,
                routing_mode="full_auto" if provider in(None, "auto") else "provider_constrained"
            )
        )
        
    return max(candidates, key=lambda x: x.score)

def stream_selected_model(user_message: str, model: str) -> Iterator[str]:
    if not user_message.strip():
        raise ValueError("user_message is required")
    if not model:
        raise ValueError("model is required")
    return stream_openrouter(user_message, model)

def stream_ai_response(user_message: str, provider: str | None = None) -> Iterator[str]:
    if not user_message.strip():
        raise ValueError("user_message is required")
    
    analysis = analyze_user_message(user_message)

    selection = resolve_selection(
        category=analysis.category,
        difficulty=analysis.difficulty,
        provider=provider,
    )

    return stream_openrouter(user_message, selection.model)

def stream_ai_response_with_meta(user_message: str, provider: str | None = None) -> tuple[Iterator[str], LLMSelection, AnalysisResult]:
    if not user_message.strip():
        raise ValueError("user_message is required")
    
    analysis = analyze_user_message(user_message)

    selection = resolve_selection(
        category=analysis.category,
        difficulty=analysis.difficulty,
        provider=provider
    )

    stream = stream_openrouter(user_message, selection.model)
    return stream, selection, analysis

    