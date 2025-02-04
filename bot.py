import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from config import *
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from handlers.trains_schedule import *

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=BOT_TOKEN)
# Диспетчер
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Расписание электричек")],
        [types.KeyboardButton(text="Расписание автобусов")],
        [types.KeyboardButton(text="Расписание маршруток")],
        [types.KeyboardButton(text="Погода")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True)
    await message.reply("Что Вас интересует?", reply_markup=keyboard)


@dp.message(F.text.lower() == "расписание электричек")
async def get_train_schedule(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Борисов - Минск")],
        [types.KeyboardButton(text="Минск - Борисов")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True)
    await message.reply("Куда держим путь?", reply_markup=keyboard)


@dp.message(F.text.lower() == "минск - борисов")
async def get_minsk_borisov_schedule(message: types.Message):
    await message.reply(await get_trains(go_from='minsk',
                                         go_to='borisov',
                                         date='03.02.2025'),
                        reply_markup=types.ReplyKeyboardRemove())


@dp.message(F.text.lower() == "борисов - минск")
async def get_borisov_minsk_schedule(message: types.Message):
    await message.reply(await get_trains(go_from='borisov',
                                         go_to='minsk',
                                         date='03.02.2025'),
                        reply_markup=types.ReplyKeyboardRemove())


@dp.message(Command("calendar"))
async def reply_calendar(message: types.Message):
    calendar = ReplyKeyboardBuilder()
    for i in range(1, 31):
        calendar.add(types.KeyboardButton(text=str(i)))
    calendar.adjust(4)
    await message.answer(
        "Выберите необходимое число,",
        reply_markup=calendar.as_markup(resize_keyboard=True)
    )

@dp.message(Command("answer"))
async def cmd_answer(message: types.Message):
    await message.answer("Это простой ответ")


@dp.message(Command("reply"))
async def cmd_reply(message: types.Message):
    await message.reply('Это ответ с "ответом"')


@dp.message(Command("dice"))
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")


@dp.message(F.text.lower() == "без пюрешки")
async def without_puree(message: types.Message):
    await message.reply("Так невкусно!")


@dp.message(Command("inline_url"))
async def cmd_inline_url(message: types.Message, bot: Bot):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="GitHub", url="https://github.com")
    )
    builder.row(types.InlineKeyboardButton(
        text="Оф. канал Telegram",
        url="tg://resolve?domain=telegram")
    )

    await message.answer(
        'Выберите ссылку',
        reply_markup=builder.as_markup(),
    )


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
