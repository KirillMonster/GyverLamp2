from GyverLamp2 import Lamp
from GyverLamp2 import GColor
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message

bot = Bot(token='TOKEN')
dp = Dispatcher(bot)

lamp = Lamp()

main_menu = [
        [KeyboardButton(text='Включить')],
        [KeyboardButton(text='Выключить')],
        [KeyboardButton(text='Следущий режим')],
        [KeyboardButton(text='Заливка')]]


@dp.message_handler(commands='start')
async def cmd_start(message: Message):
    await message.answer('Управление', reply_markup=ReplyKeyboardMarkup(keyboard=main_menu))


@dp.message_handler()
async def handler(message: types.Message):
    msg = message.text.strip().lower()
    match msg:
        case 'включить':
            lamp.turn_on()
            await message.answer('Включил', reply_markup=ReplyKeyboardMarkup(keyboard=main_menu))
        case 'выключить':
            lamp.turn_off()
            await message.answer('Выключил', reply_markup=ReplyKeyboardMarkup(keyboard=main_menu))
        case 'следущий режим':
            lamp.next_mode()
            await message.answer('Поставил', reply_markup=ReplyKeyboardMarkup(keyboard=main_menu))
        case 'заливка':
            kb = [
                [KeyboardButton(text='Красный')],
                [KeyboardButton(text='Оранжевый')],
                [KeyboardButton(text='Желтый')],
                [KeyboardButton(text='Лайм')],
                [KeyboardButton(text='Аква')],
                [KeyboardButton(text='Циан')],
                [KeyboardButton(text='Синий')],
                [KeyboardButton(text='Фиолетовый')],
                [KeyboardButton(text='Розовый')]
            ]
            await message.answer('Выбор цвета', reply_markup=ReplyKeyboardMarkup(keyboard=kb))
    if msg in GColor.colours().keys():
        lamp.color_fill(color=GColor.colours_ru2eng()[msg])
        await message.answer('Управление', reply_markup=ReplyKeyboardMarkup(keyboard=main_menu))


if __name__ == '__main__':
    executor.start_polling(dp)
