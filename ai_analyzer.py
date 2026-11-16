import openai
from config import settings
from loguru import logger

client = openai.AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY,
    timeout=15.0
)

async def analyze_tender_with_ai(title: str, description: str) -> dict:
    print("🤖 [DEBUG] Отправка запроса к OpenAI API...")
    
    prompt = f"""
    Ты — эксперт по анализу государственных и коммерческих тендеров в сфере инженерии, проектирования и строительства.
    Проанализируй следующий тендер и верни ответ строго в формате:
    РЕВЕЛАНТЕН: [Да/Нет]
    ПРИЧИНА: [Краткое обоснование на русском языке]
    СУТЬ: [Краткая выжимка технического задания в 2-3 предложениях на русском языке]

    Название тендера: {title}
    Описание: {description}
    """

    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        result_text = response.choices[0].message.content
        print("🤖 [DEBUG] Ответ от OpenAI успешно получен!")
        
        is_relevant = "ДА" in result_text.upper() or "РЕВЕЛАНТЕН: ДА" in result_text.upper()
        
        return {
            "is_relevant": is_relevant,
            "raw_analysis": result_text
        }
    except Exception as e:
        print(f"❌ [DEBUG ERROR] Ошибка OpenAI: {e}")
        logger.error(f"Ошибка при обращении к OpenAI: {e}")
        return {
            "is_relevant": False,
            "raw_analysis": f"Помилка запиту до OpenAI (таймаут/мережа): {e}"
        }