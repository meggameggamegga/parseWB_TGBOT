import asyncio
import json

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text

import config
from main import bot,dp
from keyboards.inlinekeyboard import start_keyboard, menu_inline
from sm_wb import ParseSelWB
from states.state import CheckPlace
from my_pars_wb import ParseWb


@dp.message_handler(Command('start'))
async def start_cmnd(message:types.Message):
    await message.answer('Привет, бот умеет выводить ифномрацию по заданому поисковому запросу\n'
                         'Нажми на интересующую кнопку ниже',reply_markup=start_keyboard())

@dp.message_handler(Text(equals='Показать место в карточке'))
async def check_place(message:types.Message):
    await message.answer('Введи по какому поисковому запросу искать')
    await CheckPlace.label.set()


@dp.message_handler(state=CheckPlace.label.state,content_types=types.ContentType.TEXT)
async def label_cmnd(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['label'] = message.text
    await message.answer('Теперь введи артикул своего товара')
    await CheckPlace.name.set()

#ПЕРЕДЕЛАТЬ НА АРТИКУЛ
@dp.message_handler(state=CheckPlace.name.state,content_types=types.ContentType.TEXT)
async def name_cmnd(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await bot.send_message(message.from_user.id,'Идет поиск вашего товара')
    PLACE = ParseSelWB(label=f'{data.get("label")}',article=message.text)
    result = PLACE.parse()
    print(result)
    if result !=None:
        await message.answer(f'Ваш товар находится на {result}')
    else:
        await message.answer('Товар не найден на 4 страницах. Измените артикул или слово для поиска.')



@dp.message_handler(Text(equals='Вывести информацию по запросу'))
async def take_search_info(message:types.Message):
    await message.answer('Ввидте какую информацию по запросу хотите получить')
    await CheckPlace.search.set()

@dp.message_handler(state=CheckPlace.search.state,content_types=types.ContentType.TEXT)
async def info_search(message:types.Message,state:FSMContext):
    pass


#@dp.callback_query_handler(cb_url.filter(action='menu'))
#async def get_on_card(call:types.CallbackQuery,callback_data:dict):
#    url = callback_data.get('url')




#-------Уведомление
#async def check_my_place():
#    print('Проверяю!')
#    while True:
#        WB = ParseWb(label='apple',name='iPhone 14 128GB')
#        if WB.get_place() > 2:
#            await notify_user(WB.get_place())
#        else:
#            await notify_user(place=WB.get_place(),now='yes')
#        await asyncio.sleep(60)
#
#
#async def notify_user(place,now=None):
#    if place and not now:
#        await bot.send_message(config.ADMIN_ID,'Ваше место в списке карточек изменилось.\n'
#                               f'Новое место:{place}')
#    await bot.send_message(config.ADMIN_ID,f'Ваше место в карточке все еще на {place}')