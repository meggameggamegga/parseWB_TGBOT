from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton
from aiogram.utils.callback_data import CallbackData

#cb_url = CallbackData('btn','action','url')

def start_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text='Показать место в карточке'))
    keyboard.add(KeyboardButton(text='Вывести информацию по запросу'))
    return keyboard

def menu_inline(url):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Перейти на товар',url=f'https://www.wildberries.ru/catalog/{url}/detail.aspx'))
    return keyboard