import asyncio
import os
from threading import Thread
from flask import Flask
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- НАСТРОЙКИ ---
API_TOKEN = '8297062116:AAFnnzaHxlKThy55YrX6LyGA6Miyu_BQN2A'
GHOST_PHOTO_ID = "AgACAgIAAxkBAANZahchXB9Sbur0Z0JHs3CSSMh-s5kAAmIdaxtUcrlIvV-cSHtQirQBAAMCAAN4AAM7BA"
# ID гифки (электричество)
ELECTRIC_GIF_ID = "CgACAgIAAxkBAANQahfaCKL7w336MOm1Hfxh50FbEvEAAlanAAIcZ7lInFGYbu7BHJU7BA"
# ID нового фото EGXservice
EGX_SERVICE_PHOTO_ID = "AgACAgIAAxkBAANSahfhxWhZAsAFZvhSK5jChmBs5LEAAvofaxscZ7lIMUPQ4v1bi5oBAAMCAAN5AAM7BA"

# --- WEB SERVER ---
app = Flask('')
@app.route('/')
def home(): return "Ghostix is alive!"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
Thread(target=run).start()

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- КЛАВИАТУРЫ ---
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

# --- ОБРАБОТЧИКИ ---

@dp.message(Command("start"))
async def start(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id, photo=GHOST_PHOTO_ID, 
                         caption="👻 **Здравствуй, путник...**\nЯ — Ghostix, дух мастерской EGX. Выбирай, что нужно:", 
                         reply_markup=get_main_menu())

@dp.callback_query(F.data == "start_menu")
async def back_to_start(callback: types.CallbackQuery):
    await callback.message.delete()
    await bot.send_photo(chat_id=callback.message.chat.id, photo=GHOST_PHOTO_ID, 
                         caption="👻 **Здравствуй, путник...**\nВыбирай, что нужно:", reply_markup=get_main_menu())
    await callback.answer()

# РЕМОНТ (Главный хаб)
@dp.callback_query(F.data == "service")
async def service(callback: types.CallbackQuery):
    await callback.message.delete()
    
    # Сначала анимация
    await callback.message.answer_animation(animation=ELECTRIC_GIF_ID)
    
    # Затем фото с описанием
    text = (
        "⚡️ **Добро пожаловать в EGXservice** ⚡️\n\n"
        "Здесь техника обретает вторую жизнь. Мы не просто чиним — мы восстанавливаем связь с цифровым миром.\n\n"
        "Твое устройство столкнулось с трудностями? Я здесь, чтобы помочь. "
        "Выбери категорию:"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Смартфоны/Планшеты", callback_data="serv_phones")],
        [InlineKeyboardButton(text="💻 ПК/Ноутбуки", callback_data="serv_laptops")],
        [InlineKeyboardButton(text="⚡️ Бытовая электроника", callback_data="serv_home")],
        [InlineKeyboardButton(text="⚙️ Прошивка и ПО", callback_data="serv_soft")],
        [InlineKeyboardButton(text="🔙 В главное меню", callback_data="start_menu")]
    ])
    await callback.message.answer_photo(photo=EGX_SERVICE_PHOTO_ID, caption=text, reply_markup=kb)
    await callback.answer()

# ПОДСИСТЕМЫ РЕМОНТА
@dp.callback_query(F.data.startswith("serv_"))
async def sub_service(callback: types.CallbackQuery):
    cat = callback.data.split("_")[1]
    texts = {
        "phones": "📱 **Смартфоны/Планшеты**\nДиагностика и восстановление вашего гаджета.",
        "laptops": "💻 **ПК/Ноутбуки**\nЧистка, замена деталей, апгрейд.",
        "home": "⚡️ **Бытовая электроника**\nРемонт плат и мелкой техники.",
        "soft": "⚙️ **Прошивка и ПО**\nWindows, консоли (PS/Xbox), настройка ОС."
    }
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад к ремонту", callback_data="service")]])
    await callback.message.edit_caption(caption=texts.get(cat), reply_markup=kb)

# ОСТАЛЬНЫЕ КНОПКИ
@dp.callback_query(F.data.in_({"shop", "custom", "reviews", "bonuses", "about", "support"}))
async def other_buttons(callback: types.CallbackQuery):
    data = callback.data
    content = {
        "shop": "🛒 **Каталог:** Здесь техника, прошедшая мою проверку.",
        "custom": "⚡️ **Кастом:** Индивидуальные сборки и тюнинг.",
        "reviews": "⭐ **Отзывы:** Истории тех, чью технику я спас.",
        "bonuses": "🎁 **Бонусы:** Секретные предложения для своих.",
        "about": "👤 **EGX Ghostix:** Искусство восстановления. Я тебя люблю! 😋",
        "support": "🎧 **Связь:** @onlyghostpp | +380982828598"
    }
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="start_menu")]])
    await callback.message.edit_caption(caption=content.get(data), reply_markup=kb)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
