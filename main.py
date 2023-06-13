import asyncio
from aiogram import Bot,Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

import config


bot = Bot(config.BOT_TOKEN,parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)


async def on_startup(_):
    await bot.send_message(config.ADMIN_ID,'Бот запустился')





if __name__ == '__main__':
    from handlers import dp
   # loop = asyncio.new_event_loop()
   # asyncio.set_event_loop(loop)
   # loop.create_task(check_my_place())
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
