from bs4 import BeautifulSoup
import aiohttp
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.for_questions import get_train_directions_kb


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Выберите направление",
        reply_markup=get_train_directions_kb()
    )



async def get_trains(go_from, go_to, date):
    url = f"https://poezdato.net/raspisanie-poezdov/{go_from}--{go_to}/elektrichki/{date}/"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as resp:
            schedule = ''
            page = await resp.text(encoding="utf-8")
            soup = BeautifulSoup(page, 'html.parser')
            all_headers = soup.findAll('tr')
            for header in all_headers[1:]:
                date1, date2 = header.findAll('span', class_='_time')
                result = f'Отправление {date1.text}, прибытие {date2.text}' + '\n'
                schedule += result
            return schedule

# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# def main1():
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     asyncio.run(get_trains(go_from='minsk',
#                            go_to='borisov',
#                            date='04.02.2025'))
#
#
# main1()
