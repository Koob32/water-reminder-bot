import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from config import TOKEN
from datetime import datetime


os.path.exists("water.txt")
if not os.path.exists("water.txt"):
    with open("water.txt", "w") as file:
        file.write("0")
    water_count = 0
else:
    with open("water.txt", "r") as file:
        data = file.read()
        water_count = int(data) if data else 0

now = datetime.now()
reminders_enabled = False
user_id = None
bot = Bot(token=TOKEN)
dp = Dispatcher()
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Я выпил воду")],
        #[KeyboardButton(text="💧 Выпить воду")],
        #[KeyboardButton(text="ℹ️ Помощь")],
        [KeyboardButton(text="🔔 Включить напоминания")],
        [KeyboardButton(text="🔕 Выключить напоминания")]
    ],
    resize_keyboard=True
)


@dp.message(Command("start"))
async def start(message: Message):
    global user_id
    user_id = message.chat.id

    await message.answer(
        "Привет! Я буду напоминать тебе пить воду 💧",
        reply_markup=keyboard
    )
async def water_reminder():
    while True:
        await asyncio.sleep(10)

        now = datetime.now()

        if now.hour >= 23 or now.hour < 8:
            continue

        if user_id and reminders_enabled:
            await bot.send_message(
                user_id,
                "💧 Юпик, пора выпить воды!"
            )

@dp.message(Command("water"))
async def water(message: Message):
    await message.answer(
        "💧 Якуб, пора выпить стакан воды!"
    )

@dp.message(lambda message: message.text == "🔔 Включить напоминания")
async def Pomni(message: Message):
    global reminders_enabled
    reminders_enabled = True
    await message.answer(
        "Напоминание включено 🔔"
    )

@dp.message(lambda message: message.text == "🔕 Выключить напоминания")
async def NePomni(message: Message):
    global reminders_enabled
    reminders_enabled = False
    await message.answer(
        "Напоминание выключено 🔕"
    )

@dp.message(lambda message: message.text == "✅ Я выпил воду")
async def remind_water(message: Message):
    global water_count
    water_count += 1
    with open("water.txt", "w") as file:
        file.write(str(water_count))
    await message.answer(
        f"🎉 Отлично! Ты молодец!\n"
        f"Сегодня ты выпил воды: {water_count} раз(а) 💧"
    )

@dp.message(lambda message: message.text == "💧 Выпить воду")
async def drink_water(message: Message):
    await message.answer(
        "Отлично! Иди выпей стакан воды 💪💧"
    )


@dp.message(lambda message: message.text == "ℹ️ Помощь")
async def help_command(message: Message):
    await message.answer(
        "Я помогаю тебе не забывать пить воду.\n"
        "Нажми кнопку «💧 Выпить воду», когда захочешь напомнить себе о воде."
    )

async def main():
    asyncio.create_task(water_reminder())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())