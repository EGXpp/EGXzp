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
         InlineKeyboardButton(text="⭐ Отзывы", callback_data="reviews")],
        [InlineKeyboardButton(text="🎁 Бонусы", callback_data="bonuses"),
         InlineKeyboardButton(text="👤 Кто мы?", callback_data="about")]
    ])

def get_shop_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Есть в наличии", callback_data="shop_stock")],
        [InlineKeyboardButton(text="📱 Смартфоны/планшеты", callback_data="shop_phones")],
        [InlineKeyboardButton(text="💻 Ноутбуки/ПК", callback_data="shop_laptops")],
        [InlineKeyboardButton(text="🎧 Девайсы/аксессуары", callback_data="shop_acc")],
        [InlineKeyboardButton(text="ℹ️ Доп. информация", callback_data="shop_info")],
        [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="start_menu")]
    ])

def get_service_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Смартфоны/планшеты", callback_data="serv_phones")],
        [InlineKeyboardButton(text="💻 Ноутбуки/ПК", callback_data="serv_laptops")],
        [InlineKeyboardButton(text="⚡️ Бытовая техника", callback_data="serv_home")],
        [InlineKeyboardButton(text="⚙️ Прошивка и ПО", callback_data="serv_soft")],
        [InlineKeyboardButton(text="🏢 Мастерская EGX", callback_data="workshop")],
        [InlineKeyboardButton(text="👨‍🔧 Связь с мастером", url=SUPPORT_LINK)],
        [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="start_menu")]
    ])

# --- ОБРАБОТЧИКИ ---
@dp.message(Command("start"))
async def start(message: types.Message):
    caption_text = (
        "👻 **Приветствую, путник! Я — Ghostix, дух технологий EGX.**\n\n"
        "Я здесь не просто так. Я вижу, что твоим устройствам нужно второе дыхание, а тебе — надежная техника, которая не подведет. "
        "В EGX мы не просто «чиним» или «продаем» — мы возвращаем гаджеты к жизни, наполняя их призрачной мощью и идеальной стабильностью.\n\n"
        "Что тебя ждет в моих владениях:\n"
        "🛒 **Каталог:** Техника, прошедшая мое личное ТО. Запечатана и готова к работе.\n"
        "🛠 **Ремонт:** Оживляю смартфоны, ноутбуки и любую технику.\n"
        "⚡️ **Кастом:** Сделаем твой девайс уникальным.\n"
        "⭐ **Отзывы:** Посмотри, как я уже помог другим.\n\n"
        "Выбирай направление, и давай приступим! 👇"
    )
    await bot.send_photo(chat_id=message.chat.id, photo=GHOST_PHOTO_ID, caption=caption_text, reply_markup=get_main_menu())

@dp.callback_query(F.data == "service")
async def service(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer_photo(photo=EGX_SERVICE_PHOTO_ID, 
                                        caption="🛠 **Ремонт:** Выбери услугу:", 
                                        reply_markup=get_service_menu())

@dp.callback_query(F.data == "workshop")
async def workshop(callback: types.CallbackQuery):
    await callback.answer()
    caption = (
        "🏢 **Мастерская EGX — Кузница технологий**\n\n"
        "Здесь я публикую отчеты о самых сложных операциях, оживленных «трупах» техники и кастомных доработках. "
        "Смотри, как мастерская EGX возвращает гаджеты к жизни, когда другие опускают руки!"
    )
    await callback.message.answer(caption)

@dp.callback_query(F.data == "start_menu")
async def back_to_start(callback: types.CallbackQuery):
    await callback.answer()
    await bot.send_photo(chat_id=callback.message.chat.id, photo=GHOST_PHOTO_ID, 
                         caption="👻 **Вернулись в меню:**", 
                         reply_markup=get_main_menu())

@dp.callback_query(F.data == "shop")
async def shop(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer_photo(photo=SHOP_PHOTO_ID, caption="🛒 **Каталог EGX:** Выбери категорию:", reply_markup=get_shop_menu())

@dp.callback_query(F.data == "shop_info")
async def shop_info(callback: types.CallbackQuery):
    await callback.answer()
    text = (
        "ℹ️ **О качестве и доставке EGX:**\n\n"
        "Мы не просто продаем технику — мы ее оживляем! Каждый девайс прошел полное ТО, диагностику и проверку «призраком». "
        "Мы уверены в качестве, поэтому даем **1 месяц гарантии** от себя. "
        "Хочешь спать спокойно целый год? Оформи расширенную гарантию (12 месяцев) всего за **5% от цены товара**.\n\n"
        "📦 **Доставка:**\n"
        "Товар приедет в фирменной запечатанной коробке — пломбы на месте, никто не подсматривал!\n"
        "🚀 Отправляем через: **Новую Почту, Укрпочту или OLX-доставку**.\n\n"
        "📍 **Самовывоз:**\n"
        "Мы ждем тебя в городе **Запорожье (Бабурка)**.\n\n"
        "Есть вопросы? Жми кнопку ниже и пиши нашему менеджеру — мы на связи!"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🎧 Техподдержка", url=SUPPORT_LINK)]])
    await callback.message.answer(text, reply_markup=kb)

@dp.callback_query(F.data.startswith(("shop_", "serv_")))
async def items_handler(callback: types.CallbackQuery):
    await callback.answer()
    category = callback.data.split("_")[1]
    await callback.message.answer(f"🔍 Раздел: {category.upper()}. Мастер уже уведомлен!")

@dp.callback_query(F.data.in_({"custom", "reviews", "bonuses", "about"}))
async def other_sections(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(f"Раздел {callback.data.upper()} открыт.")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
