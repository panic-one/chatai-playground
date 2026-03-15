import os
import json
from dataclasses import dataclass
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ANALYZER_MODEL = os.getenv("ANALYZER_MODEL")

AI_PROMPT = """
あなたはユーザーのメッセージを分類するAIです。
以下のJSONだけを返してください。
{
"category": "inquiry | task | reasoning | programming",
"difficulty": "low | medium | high",
"reason": "理由"
}
""".strip()


CATEGORY_SCORES = {
    "inquiry": 10,
    "task": 25,
    "reasoning": 40,
    "programming": 50,
}

DIFFICULTY_SCORES = {
    "low": 10,
    "medium": 25,
    "high": 40,
}


PROVIDER_CATEGORY_SCORE = {
    "openai": {
        "inquiry": 1,
        "task": 1,
        "reasoning": 1,
        "programming": 1,
    },

    "gemini": {
        "inquiry": 1,
        "task": 1,
        "reasoning": 1,
        "programming": 1,
    },

    "claude": {
        "inquiry": 1,
        "task": 1,
        "reasoning": 1,
        "programming": 1,
    },

    "deepseek": {
        "inquiry": 1,
        "task": 1,
        "reasoning": 1,
        "programming": 1,
    }
}

@dataclass
class AnalysisResult:
    category: str
    difficulty: str
    reason: str = ""

def analyze_user_message(user_message: str) -> AnalysisResult:
    response = client.chat.completions.create(
        model=ANALYZER_MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
           {"role": "system", "content": AI_PROMPT},
           {"role": "user", "content": user_message},
        ]
    )

    content = response.choices[0].message.content or "{}"
    
    try:
        data = json.loads(content)
    except Exception:
        return AnalysisResult(
            category="inquiry",
            difficulty="medium",
            reason="fallback",
        )

    category = data.get("category", "inquiry")
    difficulty = data.get("difficulty", "medium")
    reason = data.get("reason", "")

    if category not in {"inquiry", "task", "reasoning", "programming"}:
        category = "inquiry"

    if difficulty not in {"low", "medium", "high"}:
        difficulty = "medium"

    return AnalysisResult(
        category=category,
        difficulty=difficulty,
        reason=reason,
    )

def request_score(provider: str, category: str, difficulty: str) -> int:
    category_score = CATEGORY_SCORES.get(category, CATEGORY_SCORES["inquiry"])
    difficulty_score = DIFFICULTY_SCORES.get(difficulty, DIFFICULTY_SCORES["medium"])
    provider_score = PROVIDER_CATEGORY_SCORE.get(provider, {}).get(category, 0)

    return category_score + difficulty_score + provider_score
