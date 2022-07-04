from aiogram.utils import executor
import voice_message
from create_bot import dp, bot
from aiogram import types, Dispatcher
from handlers import client, admin, other , news_cybersport, news_ixbt , casino_spin
from data_base import sqlite_db
from voice_message import voice
from keyboards import client_kb
from aiogram.utils.markdown import hbold,hunderline,hcode,hlink
import psycopg2 as sq


voice.register_handlers_voice(dp)
# <---------Новости----------->
news_cybersport.register_handlers_news(dp)
news_ixbt.register_handlers_news(dp)
#<---------------------------->
casino_spin.register_handlers_casino(dp)
client.register_handlers_client(dp)
client_kb.register_callback_query(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)

    

async def on_startup(_):
    me=await bot.get_me()
    print('\033[33m' +'[~] Bot '+'\033[0m'+'\033[39m' + me.first_name +'\033[0m' + '\033[33m'+' start!'+'\033[0m')
    sqlite_db.sql_start()
    
    
async def commands_list_menu(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Регистрация"),
        types.BotCommand("wiki","поиск в википедии"),
        types.BotCommand("img","рандомная картинка по запросу"),
        types.BotCommand("gif","гифка рандомная"),
        types.BotCommand("voice","озвучка текста"),
        types.BotCommand("reg", "регистрация"),
        types.BotCommand("profs","регистрация"),
        types.BotCommand("casino","казино"),
        types.BotCommand("balance","баланс"),
        types.BotCommand("cybersport","игровые новости"),
        types.BotCommand("@C_K_1_bot","поиск в ютубе"),
        types.BotCommand("@C_K_1_bot gif","поиск в гифки"),
    ])


executor.start_polling(dp, skip_updates=True,on_startup=on_startup)