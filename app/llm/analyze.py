import os
import json
from dataclasses import dataclass
from openai import OpenAI, OpenAIError

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ANALYZER_MODEL = os.getenv("ANALYZER_MODEL")
if not ANALYZER_MODEL:
    raise RuntimeError(
        "ANALYZER_MODEL environment variable is not set."
        "Please configure an analyzer model to use with the OpenAI client"
    )

CATEGORIES = ("inquiry", "writing", "translation", "reasoning", "programming")
DIFFICULTIES = ("low", "medium", "high")

AI_PROMPT = """
あなたはユーザーのメッセージを分類するAIです。
以下のJSONだけを返してください。
{{
"category": "{categories}",
"difficulty": "{difficulties}",
"reason": "理由"
}}

分類ルール:
category:
- inquiry: 単純な質問、事実確認
- translation: 翻訳や要約
- writing: 文章生成
- reasoning: 論理的な推論
- programming: プログラミングに関するコード生成、デバッグ、設計、アルゴリズム

difficulty:
- low:一般的な知識で即答できる単純な質問
- medium:複数の情報を組み合わせたり、ある程度の専門知識や手順を要する依頼
- high:高度な専門知識、複雑な論理的思考を必要とする依頼

例:
- 入力: 1+1を答えて 
- 出力: {{"category": "inquiry", "difficulty": "low", "reason": "単純な計算"}}

- 入力: この文章英語に翻訳して 
- 出力: {{"category": "translation", "difficulty": "low", "reason": "翻訳タスク"}}

- 入力: Pythonで二分探索のコードを書いて 
- 出力: {{"category": "programming", "difficulty": "medium", "reason": "アルゴリズム"}}

""".format(
    categories=" | ".join(CATEGORIES),
    difficulties=" | ".join(DIFFICULTIES),
)

CATEGORY_SCORES = {
    "inquiry": 10,
    "translation": 20,
    "writing": 30,
    "reasoning": 40,
    "programming": 50,
}

DIFFICULTY_SCORES = {
    "low": 10,
    "medium": 25,
    "high": 40,
}

@dataclass
class AnalysisResult:
    category: str
    difficulty: str
    reason: str = ""

def analyze_user_message(user_message: str) -> AnalysisResult:
    if not user_message or not user_message.strip():
        return AnalysisResult(
            category="inquiry",
            difficulty="medium",
            reason="fallback",
        )
    
    try:
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
        data = json.loads(content)
    except OpenAIError:
        return AnalysisResult(
            category="inquiry",
            difficulty="medium",
            reason="fallback",
        )
    except Exception:
        return AnalysisResult(
            category="inquiry",
            difficulty="medium",
            reason="fallback"
        )

    category = data.get("category", "inquiry")
    difficulty = data.get("difficulty", "medium")
    reason = str(data.get("reason", "")).strip()
    if not reason:
        reason = "分類理由がありません"

    if category not in CATEGORIES:
        category = "inquiry"

    if difficulty not in DIFFICULTIES:
        difficulty = "medium"

    return AnalysisResult(
        category=category,
        difficulty=difficulty,
        reason=reason,
    )

def request_score(category: str, difficulty: str) -> int:
    category_score = CATEGORY_SCORES.get(category, CATEGORY_SCORES["inquiry"])
    difficulty_score = DIFFICULTY_SCORES.get(difficulty, DIFFICULTY_SCORES["medium"])

    return category_score + difficulty_score
