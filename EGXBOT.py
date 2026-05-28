from flask import Flask
from threading import Thread
import os

app = Flask('')

@app.route('/')

def home():
    return "Ghostix is alive!"

def run():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '8297062116:AAFnnzaHxlKThy55YrX6LyGA6Miyu_BQN2A'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

GHOST_PHOTO_ID = "AgACAgIAAxkBAANZahchXB9Sbur0Z0JHs3CSSMh-s5kAAmIdaxtUcrlIvV-cSHtQirQBAAMCAAN4AAM7BA"

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

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id, photo=GHOST_PHOTO_ID)
    
    text = (
        "👻 **Здравствуй, путник...**\n\n"
        "Ты слышишь этот легкий гул электричества? Это я — Ghostix. Я не просто призрак, я — дух, живущий в микросхемах и проводах мастерской EGX.\n\n"
        "Я здесь, чтобы помогать таким, как ты, восстанавливать связь с цифровым миром. Пока остальные боятся поломок, я нахожу в них новую жизнь. Мой дом — это Запорожье, Бабурка, и сегодня мой дом открыт для тебя.\n\n"
        "Ты зашел в цифровое пространство, где техника обретает бессмертие. Здесь тебя не ждут скучные инструкции — здесь тебя ждет экспертный ремонт, кастомные решения и честный сервис. Я лично прослежу, чтобы каждый винтик был на своем месте.\n\n"
        "Выбирай, что тебе нужно, чтобы мы могли начать?"
    )
    await message.answer(text, reply_markup=get_main_menu())

@dp.callback_query(F.data == "support")
async def support(callback: types.CallbackQuery):
    await callback.message.answer("🎧 **Техподдержка:**\n💬 @onlyghostpp\n📞 +380982828598\n\nЯ на связи, не стесняйся!")
    await callback.answer()

@dp.callback_query(F.data == "shop")
async def shop(callback: types.CallbackQuery):
    await callback.message.answer("🛒 **Каталог:** Здесь техника, прошедшая мою проверку. Никаких «призрачных» дефектов!")
    await callback.answer()

@dp.callback_query(F.data == "service")
async def service(callback: types.CallbackQuery):
    await callback.message.answer("🛠 **Ремонт:** Оживляю гаджеты, от которых отказались другие.")
    await callback.answer()

@dp.callback_query(F.data == "custom")
async def custom(callback: types.CallbackQuery):
    await callback.message.answer("⚡️ **Кастом:** Индивидуальные сборки аккумуляторов. Мощность, которая не заканчивается.")
    await callback.answer()

@dp.callback_query(F.data == "reviews")
async def reviews(callback: types.CallbackQuery):
    await callback.message.answer("⭐ **Отзывы:** Истории тех, чью технику я спас. Твоя история может стать следующей!")
    await callback.answer()

@dp.callback_query(F.data == "bonuses")
async def bonuses(callback: types.CallbackQuery):
    await callback.message.answer("🎁 **Бонусы:** Секретные предложения для постоянных гостей мастерской EGX. Следи за обновлениями!")
    await callback.answer()

@dp.callback_query(F.data == "about")
async def about(callback: types.CallbackQuery):
    await callback.message.answer("👤 **EGX Ghostix:** Мы — больше, чем сервис. Это искусство восстановления.\n\nКИСУНИЧКА, Я ТЕБЯ БЕЗУМНО СИЛЬНО ЛЮБЛЮ!😋🥰")
    await callback.answer()

async def main():
    print("Бот Ghostix запущен!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
