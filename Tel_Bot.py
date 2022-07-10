import asyncio
from aiogram.utils import executor
import voice_message
from create_bot import dp, bot
from aiogram import types, Dispatcher
from handlers import client, admin, other , news_cybersport, news_ixbt , casino_spin,ls_message
from data_base import sqlite_db,cripts_price_change
from voice_message import voice
from keyboards import client_kb
from aiogram.utils.markdown import hbold,hunderline,hcode,hlink
import psycopg2 as sq


voice.register_handlers_voice(dp)
ls_message.register_handlers_ls_message(dp)
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
    # await bot.send_message(chat_id=1133903696,text='[~] Bot start!')
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

if __name__ =='__main__':
    # <---------Заготовка под изменение крипт----------->
    loop=asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(cripts_price_change.cripts_price_change())# тут в () указать название класса def для запустка цикла
    #<-------------------------------------------------->
    executor.start_polling(dp, skip_updates=True,on_startup=on_startup)