from aiogram import types, executor, Bot, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import WeatherAPI as wAPI
import utility
import pandas as pd

# API Токен для бота
TOKEN_API = ''

# Создаем самого бота, хранилище памяти и обработчика сообщений
storage = MemoryStorage()
bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=storage)

city_table = pd.read_csv('cities.csv')
days_table = pd.read_csv('days.csv')


# Список состояний бота
class ProfileStatesGroup(StatesGroup):
    upl_city = State()
    upl_day = State()
    finish = State()


def get_city_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in range(len(city_table)):
        button = KeyboardButton(city_table.values[i][0])
        kb.add(button)

    return kb


def get_day_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in range(len(days_table)):
        button = KeyboardButton(days_table.values[i][0])
        kb.add(button)

    return kb


def start_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton('/start'))

    return kb


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.message) -> None:
    await message.answer(text='Добро пожаловать\n в WeatherAPI Bot! Укажите город, в котором хотите узнать погоду',
                         reply_markup=get_city_kb())
    await ProfileStatesGroup.upl_city.set()


@dp.message_handler(state=ProfileStatesGroup.upl_city)  # content_types=['text']
async def upload_weight(message: types.message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['city_ru'] = message.text
        data['city'] = utility.find_in_csv_dict_table(city_table, message.text)

    if utility.check_in_csv_dict_table(city_table, message.text):
        await message.answer(text=f'Хорошо. Ваш город: {data["city_ru"]}. На какой день вы хотите узнать погоду?',
                             reply_markup=get_day_kb())
        await ProfileStatesGroup.next()

    else:
        await message.answer(text=f'Похоже, вы не выбрали кнопку! Попробуйте ещё раз!')
        await message.answer(text='Добро пожаловать\n в WeatherAPI Bot! Укажите город, в котором хотите узнать погоду',
                             reply_markup=get_city_kb())
        await ProfileStatesGroup.next()
        await ProfileStatesGroup.previous()


# Тут будет присылаться погода
@dp.message_handler(state=ProfileStatesGroup.upl_day)  # content_types=['text']
async def upload_weight(message: types.message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['day_ru'] = message.text
        data['day_id'] = utility.find_in_csv_dict_table(days_table, message.text)

    if utility.check_in_csv_dict_table(days_table, message.text):
        await message.answer(text=f'Погода в городе {data["city_ru"]} {data["day_ru"].lower()}:\n'
                                  f'{wAPI.get_weather_for_date(data["city"],int(data["day_id"]))}',
                             reply_markup=start_kb(), parse_mode="HTML")

        await state.finish()
    else:
        await message.answer(text=f'Похоже, вы не выбрали кнопку! Попробуйте ещё раз!')
        await message.answer(text=f'Хорошо. Ваш город: {data["city_ru"]}. На какой день вы хотите узнать погоду?',
                             reply_markup=get_day_kb())
        await ProfileStatesGroup.next()
        await ProfileStatesGroup.previous()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
