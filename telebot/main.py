import asyncio
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv  # импортируем токен
import logging

load_dotenv()
BOT_TOKEN = os.getenv('token', 'no secrets')

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)


class Storage:
    data: dict

    def __init__(self) -> None:
        self.data = {}

    def set(self, name: str, value: any) -> None:
        self.data[name] = value

    def get(self, name: str) -> any:
        return self.data[name]


storage = Storage()

# создаем диспетчер
dp = Dispatcher()

poem = ('Опять, как в годы золотые,\nТри стертых треплются шлеи,\nИ вязнут спицы расписные\nВ расхлябанные '
        'колеи…\nРоссия, нищая Россия,\nМне избы серые твои,\nТвои мне песни ветровые,-\nКак слезы первые '
        'любви!\nТебя жалеть я не умею\nИ крест свой бережно несу…\nКакому хочешь чародею\nОтдай разбойную '
        'красу!\nПускай заманит и обманет,-\nНе пропадешь, не сгинешь ты,\nИ лишь забота затуманит\nТвои прекрасные '
        'черты…\nНу что ж? Одной заботой боле —\nОдной слезой река шумней\nА ты все та же — лес, да поле,'
        '\nДа плат узорный до бровей…\nИ невозможное возможно,\nДорога долгая легка,\nКогда блеснет в дали '
        'дорожной\nМгновенный взор из-под платка,\nКогда звенит тоской острожной\nГлухая песня ямщика!..')


async def main():
    bot = Bot(token=BOT_TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


@dp.message(F.text == 'ДА')
@dp.message(Command('start'))  # декоратор для обработчика команды start
async def process_start_command(message: types.Message):
    reply_keyboard = [[KeyboardButton(text='/suphler')]]
    kb = ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True, one_time_keyboard=False)
    storage.set('num_row', 0)
    """
    Создаем и регистрируем в диспетчере асинхронный обработчик сообщений.
    В параметре message содержится вся информация о сообщении - см. документацию.
    """
    row = poem.split('\n')[storage.data['num_row']]
    await message.answer(
        f"Здравствуйте!\nЯ телеграмм бот-литератор. Вот первая строка стихотворения:\n\n{row}",
        reply_markup=kb)  # отправляет
    # ответ на сообщение


@dp.message(Command('suphler'))  # декоратор для обработчика команды start
async def process_start_command(message: types.Message):
    row = poem.split('\n')[storage.data['num_row'] + 1]
    await message.answer(
        f"Подсказка: следующая строка стихотворения:\n\n{row}")  # отправляет


@dp.message(F.text == 'НЕТ')
@dp.message(Command('stop'))  # декоратор для обработчика команды start
async def process_start_command(message: types.Message):
    storage.data['num_row'] = 0
    await message.answer(
        f"Хорошо")  # отправляет


@dp.message()
async def process_start_command(message: types.Message):
    try:
        row = poem.split('\n')[storage.data['num_row'] + 1]
        if message.text == row:
            storage.data['num_row'] += 2
            row = poem.split('\n')[storage.data['num_row']]
            await message.reply(f"Правильно!\nВот следующая строка стихотворения:\n\n{row}")
            # ответ на сообщение
        else:
            await message.answer(f'нет, не так! Для подсказки используйте команду /suphler')
    except IndexError:
        reply_keyboard = [[KeyboardButton(text='ДА')], [KeyboardButton(text='НЕТ')]]
        kb = ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True, one_time_keyboard=False)
        storage.data['num_row'] = 0
        await message.answer(f'Отлично! Я очень рад, что вы знаете это стихотворение! Не хотите повторить?',
                             reply_markup=kb)


if __name__ == '__main__':
    asyncio.run(main())  # начинаем принимать сообщения
