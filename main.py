import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandStart
from handlers import user_router, send_message
from createBot import bot
from database import create_table
from apscheduler.schedulers.asyncio import AsyncIOScheduler
#from database import on_startup
dp = Dispatcher()

dp.include_router(user_router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    #await on_startup()
    await create_table()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_message, "interval", days=1, args=(dp,)) #days = 1
    scheduler.start()
    await dp.start_polling(bot)
    
    

if __name__ == "__main__": 
    asyncio.run(main())
    
