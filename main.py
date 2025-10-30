import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

# ✅ Токен жана админ ID
BOT_TOKEN = "8229688155:AAFGOL61nBlTGp05CGhxjwVUxhoC9MQeiyM"
ADMIN_ID = 1900213029

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ✅ FSM абалдары
class Form(StatesGroup):
    waiting_for_text = State()

# ✅ Баштапкы меню
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()  # абалды тазалоо

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="😔 Даттануу"), KeyboardButton(text="💡 Сунуш")],
            [KeyboardButton(text="🗣 Идея"), KeyboardButton(text="ℹ️ Маалымат")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "👋 *Саламатсызбы!* Мени пайдаланып кайрылсаңыз болот👇",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

# ✅ Категория тандалганда
@dp.message(F.text.in_(["😔 Даттануу", "💡 Сунуш", "🗣 Идея"]))
async def choose_category(message: Message, state: FSMContext):

    categories = {
        "😔 Даттануу": "📢 *Даттануу бөлүмү:*\nМектептеги көйгөйлөрдү же адилетсиздикти жазыңыз.\n\n✍️ Даттанууңузду жазыңыз:\n\nНомериңизди калтырганды унутпаңыз биз сиз менен байланышыбыз:",
        "💡 Сунуш": "💡 *Сунуш бөлүмү:*\nМектепти жакшыртуу боюнча сунушуңузду жазыңыз.\n\n✍️ Сунушуңузду жазыңыз:\n\nНомериңизди калтырганды унутпаңыз биз сиз менен байланышыбыз:",
        "🗣 Идея": "🌟 *Идеялар бөлүмү:*\нМектептик иш-чара, долбоор боюнча идеяңызды жазыңыз.\n\n✍️ Идеяңызды жазыңыз:\n\nНомериңизди калтырганды унутпаңыз биз сиз менен байланышыбыз:"
    }

    await state.update_data(category=message.text)
    await state.set_state(Form.waiting_for_text)

    await message.answer(categories[message.text])

# ✅ ℹ️ Маалымат
@dp.message(F.text == "ℹ️ Маалымат")
async def info(message: Message):
    await message.answer(
        "ℹ️ *Маалымат:*\n"
        "Жазылган билдирүү купуя сакталат жана администрацияга жөнөтүлөт ✅\n\n"
        "📞 Байланыш: 0708974785",
        parse_mode="Markdown"
    )

# ✅ Колдонуучунун билдирүүсүн кабыл алып админге жөнөтүү
@dp.message(Form.waiting_for_text)
async def forward_to_admin(message: Message, state: FSMContext):
    user_data = await state.get_data()
    category = user_data.get("category", "Белгисиз категория")

    admin_msg = (
        "📩 *Жаңы билдирүү!*\n\n"
        f"📌 Категория: {category}\n"
        f"👤 Колдонуучу: {message.from_user.full_name}\n"
        f"🆔 ID: `{message.from_user.id}`\n\n"
        f"💬 Текст:\n{message.text}"
    )

    await bot.send_message(ADMIN_ID, admin_msg, parse_mode="Markdown")

    await message.answer(
        "✅ Рахмат! Билдирүү жөнөтүлдү.\n"
        "Жооп шашылыш каралат.",
        parse_mode="Markdown"
    )

    await state.clear()


# ✅ Ботту иштетүү
async def main():
    print("🤖 Бот иштеп жатат...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
