import asyncio
import os
from threading import Thread
from flask import Flask
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '8297062116:AAFnnzaHxlKThy55YrX6LyGA6Miyu_BQN2A'
GHOST_PHOTO_ID = "AgACAgIAAxkBAANZahchXB9Sbur0Z0JHs3CSSMh-s5kAAmIdaxtUcrlIvV-cSHtQirQBAAMCAAN4AAM7BA"
EGX_SERVICE_PHOTO_ID = "AgACAgIAAxkBAAIBI2oX7UrebOf2w_kgBRASZtetfyalAAL6H2sbHGe5SJDDRgo4Dgx1AQADAgADeQADOwQ"

app = Flask('')
@app.route('/')
def home(): return "Ghostix is alive!"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
Thread(target=run).start()

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def get_main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Каталог", callback_data="shop"),
         InlineKeyboardButton(text="🛠 Ремонт", callback_data="service")],
        [InlineKeyboardButton(text="⚡️ Кастом", callback_data="custom"),
         InlineKeyboardButton(text="⭐ Отзывы", callback_data="reviews")],
        [InlineKeyboardButton(text="🎁 Бонусы", callback_data="bonuses"),
         InlineKeyboardButton(text="👤 Кто мы?", callback_data="about")],
        [InlineKeyboardButton(text="🎧 Связь с мастером", callback_data="support")]
    ])

def get_service_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Смартфоны/Планшеты", callback_data="serv_phones")],
        [InlineKeyboardButton(text="💻 ПК/Ноутбуки", callback_data="serv_laptops")],
        [InlineKeyboardButton(text="⚡️ Бытовая техника", callback_data="serv_home")],
        [InlineKeyboardButton(text="⚙️ Прошивка и ПО", callback_data="serv_soft")],
        [InlineKeyboardButton(text="🔙 В главное меню", callback_data="start_menu")]
    ])

@dp.message(Command("start"))
async def start(message: types.Message):
    text = (
        "👻 **Здравствуй, путник из цифровой пустоты...**\n\n"
        "Я — Ghostix, дух и верховный архитектор мастерской **EGX**. "
        "Когда-то я был лишь потоком данных, но теперь обрел форму, чтобы стать "
        "твоим проводником в мир идеальной работы техники.\n\n"
        "**Что такое EGX?**\n"
        "Это точка сингулярности, где железо перестает страдать, а электроника "
        "обретает вторую молодость. Мы не просто чиним — мы устраняем хаос.\n\n"
        "**Что тебя ждет здесь?**\n"
        "• Глубинная диагностика каждой детали.\n"
        "• Восстановление на компонентном уровне.\n"
        "• Гарантия, которую дает сам дух мастерской.\n\n"
        "Выбери свой путь восстановления:"
    )
    await bot.send_photo(chat_id=message.chat.id, photo=GHOST_PHOTO_ID, caption=text, reply_markup=get_main_menu())

@dp.callback_query(F.data == "start_menu")
async def back_to_start(callback: types.CallbackQuery):
    await callback.answer()
    text = "👻 **Ты снова в обители EGX.**\nВыбери, какое направление требует моего внимания:"
    await bot.send_photo(chat_id=callback.message.chat.id, photo=GHOST_PHOTO_ID, caption=text, reply_markup=get_main_menu())

@dp.callback_query(F.data == "service")
async def service(callback: types.CallbackQuery):
    await callback.answer()
    text = (
        "⚡️ **EGXservice: Лаборатория воскрешения** ⚡️\n\n"
        "Здесь техника проходит через горнило восстановления. Выбери категорию, "
        "соответствующую твоему устройству:"
    )
    await callback.message.answer_photo(photo=EGX_SERVICE_PHOTO_ID, caption=text, reply_markup=get_service_menu())

@dp.callback_query(F.data.startswith("serv_"))
async def sub_service(callback: types.CallbackQuery):
    cat = callback.data.split("_")[1]
    texts = {
        "phones": "📱 **Смартфоны:** Разбитые экраны и уставшие аккумуляторы — я верну им яркость и мощь.",
        "laptops": "💻 **ПК/Ноутбуки:** Избавлю от шума, пыли и программных тормозов. Заставлю летать!",
        "home": "⚡️ **Бытовая техника:** Верну к жизни приборы, от которых отказались остальные.",
        "soft": "⚙️ **ПО:** Ошибки, зависания и вирусы — это лишь шум. Настрою как часы."
    }
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад к услугам", callback_data="service")]])
    await callback.message.answer(texts.get(cat, "Раздел выбран."), reply_markup=kb)

@dp.callback_query(F.data.in_({"shop", "custom", "reviews", "bonuses", "about", "support"}))
async def other_buttons(callback: types.CallbackQuery):
    data = callback.data
    content = {
        "shop": "🛒 **Витрина EGX:** Только проверенная техника. Каждое устройство здесь как новое.",
        "custom": "⚡️ **Кастом:** Сделаю твое устройство уникальным и мощным, на зависть всем.",
        "reviews": "⭐ **Свиток благодарностей:** История тех, чью технику я спас. Радость клиентов — моя энергия.",
        "bonuses": "🎁 **Артефакты:** Секретные предложения и бонусы для своих. Заглядывай чаще!",
        "about": "👤 **EGX Ghostix:** Я — воплощение мастерства. Искусство восстановления — это моя миссия.",
        "support": "🎧 **Прямая линия:** @onlyghostpp | Мастер всегда на связи, чтобы решить любой твой вопрос."
    }
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 В главное меню", callback_data="start_menu")]])
    await callback.message.answer(content.get(data), reply_markup=kb)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
