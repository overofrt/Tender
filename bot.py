import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select
from config import settings
from database import async_session_maker
from models import TenderDB
from ai_analyzer import analyze_tender_with_ai

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="📋 Актуальные тендеры", callback_data="list_tenders"),
        types.InlineKeyboardButton(text="🔍 Проверить новые", callback_data="check_new")
    )
    builder.row(
        types.InlineKeyboardButton(text="⚙️ Статус системы", callback_data="status")
    )
    return builder.as_markup()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать в систему мониторинга тендеров (Грузия)!\n\n"
        "Я отслеживаю инженерные и инфраструктурные закупки, анализирую их с помощью AI и присылаю только релевантные предложения.\n\n"
        "Используйте кнопки ниже для навигации:",
        reply_markup=get_main_menu()
    )
    
    @dp.callback_query(F.data == "check_new")
async def process_check_new(callback: types.CallbackQuery):
    await callback.answer()       
    chat_id = callback.message.chat.id

    await callback.message.answer("⏳ Запускаю проверку и AI-анализ новых тендеров...")
    ...

@dp.callback_query(F.data == "status")
async def process_status(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🟢 Система работает в штатном режиме.\n"
        "• База данных: Подключена (SQLite)\n"
        "• AI-модуль (OpenAI): Активен\n"
        "• Зона поиска: Грузия (инженерия / строительство)",
        reply_markup=get_main_menu()
    )
    await callback.answer()

@dp.callback_query(F.data == "list_tenders")
async def process_list_tenders(callback: types.CallbackQuery):
    async with async_session_maker() as session:
        result = await session.execute(
            select(TenderDB).order_by(TenderDB.created_at.desc()).limit(5)
        )
        tenders = result.scalars().all()

    if not tenders:
        await callback.message.edit_text(
            "📭 В базе данных пока нет сохраненных тендеров.\nНажмите «Проверить новые», чтобы запустить симуляцию сбора.",
            reply_markup=get_main_menu()
        )
        await callback.answer()
        return

    text = "📋 Последние сохраненные тендеры:\n\n"
    for t in tenders:
        text += f"🔹 {t.title}\n💰 Бюджет: {t.budget} {t.currency}\n🔗 {t.source_url}\n\n"

    await callback.message.edit_text(text, reply_markup=get_main_menu(), disable_web_page_preview=True)
    await callback.answer()

@dp.callback_query(F.data == "check_new")
async def process_check_new(callback: types.CallbackQuery):
    chat_id = callback.message.chat.id
    
    await callback.message.answer("⏳ Запускаю проверку и AI-анализ новых тендеров...")
    
    try:
        unique_id = random.randint(10000, 99999)
        sample_title = f"Строительство мостового перехода №{unique_id} в регионе Кахети"
        sample_desc = "Требуется выполнить проектно-изыскательные и строительные работы по возведению моста, прокладке дренажных сетей и дорожного полотна."
        

        ai_result = await analyze_tender_with_ai(sample_title, sample_desc)
        
        async with async_session_maker() as session:
            new_tender = TenderDB(
                tender_number=f"GEO-2026-{unique_id}",
                title=sample_title,
                customer="Департамент автомобильных дорог Грузии",
                description=sample_desc,
                budget=450000.0,
                currency="GEL",
                source_url="https://tenders.procurement.gov.ge",
                platform="procurement.gov.ge",
                is_relevant=ai_result["is_relevant"],
                ai_summary=ai_result["raw_analysis"]
            )
            session.add(new_tender)
            await session.commit()

        await bot.send_message(
            chat_id=chat_id,
            text=(
                f"✅ Проверка завершена!\n\n"
                f"Найден новый тендер:\n"
                f"📌 {sample_title}\n\n"
                f"🤖 Результат AI-анализа:\n{ai_result['raw_analysis']}"
            ),
            reply_markup=get_main_menu()
        )

    except Exception as e:
        await bot.send_message(
            chat_id=chat_id,
            text=f"❌ **Ошибка во время исполения:**\n<code>{str(e)}</code>",
            parse_mode="HTML",
            reply_markup=get_main_menu()
        )

    await callback.answer()
