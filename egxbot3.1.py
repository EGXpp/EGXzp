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
SHOP_PHOTO_ID = "AgACAgIAAxkBAAIB4WohNu3ZqScouMuT20ZihXs3r0dZAAJcGWsbCR4JSRQTRW4GGJFOAQADAgADeQADOwQ"

SUPPORT_LINK = "https://t.me/ТВОЙ_НИК"

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
         InlineKeyboardButton(text="🎁 Бонусы", callback_data="bonuses")],
        [InlineKeyboardButton(text="👤 Кто мы?", callback_data="about")]
    ])

def get_shop_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ В наличии", callback_data="shop_stock")],
        [InlineKeyboardButton(text="📱 Смартфоны/планшеты", callback_data="shop_phones")],
        [InlineKeyboardButton(text="💻 ПК/Ноутбуки", callback_data="shop_laptops")],
        [InlineKeyboardButton(text="🎧 Девайсы/аксессуары", callback_data="shop_acc")],
        [InlineKeyboardButton(text="🔥 Горячие предложения", callback_data="shop_hot")],
        [InlineKeyboardButton(text="👨‍💻 Менеджер", url=SUPPORT_LINK)],
        [InlineKeyboardButton(text="ℹ️ Подробно про EGX Shop", callback_data="shop_info")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="start_menu")]
    ])

def get_service_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Смартфоны/планшеты", callback_data="serv_phones")],
        [InlineKeyboardButton(text="💻 Ноутбуки/ПК", callback_data="serv_laptops")],
        [InlineKeyboardButton(text="🏢 Мастерская EGX", callback_data="workshop")],
        [InlineKeyboardButton(text="👨‍🔧 Связь с мастером", url=SUPPORT_LINK)],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="start_menu")]
    ])

# --- ОБРАБОТЧИКИ ---
@dp.message(Command("start"))
async def start(message: types.Message):
    caption = "👻 Привет, путник! Я — Ghostix, дух технологий EGX. Выбирай направление:"
    await bot.send_photo(chat_id=message.chat.id, photo=GHOST_PHOTO_ID, caption=caption, reply_markup=get_main_menu())

@dp.callback_query(F.data == "shop")
async def shop(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer_photo(photo=SHOP_PHOTO_ID, caption="🛒 **Каталог EGX.** Твой выбор:", reply_markup=get_shop_menu())

@dp.callback_query(F.data == "service")
async def service(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer_photo(photo=EGX_SERVICE_PHOTO_ID, caption="🛠 **Сервисный центр EGX.** Что нужно починить?", reply_markup=get_service_menu())

@dp.callback_query(F.data == "workshop")
async def workshop(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("🏢 **Мастерская EGX:** Отчеты о самых сложных операциях и кастомных доработках.")

@dp.callback_query(F.data.startswith(("shop_", "serv_")))
async def items_handler(callback: types.CallbackQuery):
    await callback.answer()
    category = callback.data.split("_")[1]
    await callback.message.answer(f"🔍 Раздел: {category.upper()}. Мастер уже уведомлен!")

@dp.callback_query(F.data.in_({"custom", "bonuses", "about"}))
async def other_sections(callback: types.CallbackQuery):
    await callback.answer()
    text = {"custom": "⚡️ **Кастом:** Твой девайс — твои правила.", "bonuses": "🎁 **Бонусы:** Скидки и акции для своих.", "about": "👤 **Кто мы?** Команда EGX, возвращающая жизнь технике!"}
    await callback.message.answer(text.get(callback.data))

@dp.callback_query(F.data == "start_menu")
async def back_to_start(callback: types.CallbackQuery):
    await callback.answer()
    await bot.send_photo(chat_id=callback.message.chat.id, photo=GHOST_PHOTO_ID, caption="👻 Меню:", reply_markup=get_main_menu())

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
