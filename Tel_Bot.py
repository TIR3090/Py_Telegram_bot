from aiogram.utils import executor
import voice_message
from create_bot import dp, bot
from aiogram import types, Dispatcher
from handlers import client, admin, other
from data_base import sqlite_db
from voice_message import voice
import psycopg2 as sq


voice.register_handlers_voice(dp)
client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)

    

async def on_startup(_):
    me=await bot.get_me()
    print('\033[33m' +'[~] Bot '+'\033[0m'+'\033[39m' + me.first_name +'\033[0m' + '\033[33m'+' start!'+'\033[0m')
    sqlite_db.sql_start()
    
    
async def commands_list_menu(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "для тестов"),
        types.BotCommand("reg", "регистрация"),
        types.BotCommand("profs","регистрация"),
    ])


executor.start_polling(dp, skip_updates=True,on_startup=on_startup)