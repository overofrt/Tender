import re
import httpx
from config import settings
from loguru import logger

MODEL = "gemini-flash-lite-latest"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent"


async def analyze_tender_with_ai(title: str, description: str) -> dict:
    logger.info("Отправка запроса к Gemini API...")

    prompt = f"""
    Ты — эксперт по анализу государственных и коммерческих тендеров в сфере инженерии, проектирования и строительства.
    Проанализируй следующий тендер и верни ответ строго в формате:
    РЕЛЕВАНТЕН: [Да/Нет]
    ПРИЧИНА: [Краткое обоснование на русском языке]
    СУТЬ: [Краткая выжимка технического задания в 2-3 предложениях на русском языке]

    Название тендера: {title}
    Описание: {description}
    """

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                URL,
                headers={"x-goog-api-key": settings.GEMINI_API_KEY},
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "temperature": 0.3,
                        "thinkingConfig": {"thinkingBudget": 0},
                    },
                },
            )
            response.raise_for_status()
            data = response.json()

        result_text = data["candidates"][0]["content"]["parts"][0]["text"]
        is_relevant = bool(
            re.search(r"РЕЛЕВАНТЕН:\s*\**\s*ДА", result_text.upper())
        )
        return {"is_relevant": is_relevant, "raw_analysis": result_text}

    except Exception as e:
        logger.error(f"Ошибка при обращении к Gemini: {type(e).__name__}: {e!r}")
        return {
            "is_relevant": False,
            "raw_analysis": "Помилка запиту до AI. Деталі дивіться в логах Render.",
        }
