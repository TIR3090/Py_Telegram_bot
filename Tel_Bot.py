import asyncio
from aiogram.utils import executor
from config import TOKEN,DEVELOPER
import voice_message
from create_bot import dp, bot
from aiogram import types, Dispatcher
from handlers import client, admin, other ,\
    news_cybersport, news_ixbt , casino_spin,ls_message,registration,bonus_chy,commands_list_menu,\
    img_random,search_wiki,gif_random,info_profile_reply,cripts_menu
from cripts_buy_and_sell import bitcoin_valuta_selection_buy,buy_btc_chy,buy_btc_usd,cancel_handler_cripts_buy,\
    cancel_handler_cripts_sell,ethereum_valuta_selection_buy,buy_eth_chy,buy_eth_usd,bitcoin_valuta_selection_sell,\
    sell_btc_chy,sell_btc_usd,ethereum_valuta_selection_sell,sell_eth_chy,sell_eth_usd
from data_base import sqlite_db,cripts_price_change
from voice_message import voice
from keyboards import help_kb
from aiogram.utils.markdown import hbold,hunderline,hcode,hlink
import psycopg2 as sq



#<---------------------------------------------------------->
registration.register_handlers_registration(dp)
commands_list_menu.register_handlers_commands_list_menu(dp)
bitcoin_valuta_selection_buy.register_handlers_buy_btc_usd_chy(dp)
bitcoin_valuta_selection_sell.register_handlers_sell_btc_usd_chy(dp)
ethereum_valuta_selection_buy.register_handlers_buy_eth_usd_chy(dp)
ethereum_valuta_selection_sell.register_handlers_sell_eth_usd_chy(dp)
cancel_handler_cripts_buy.register_handlers_cancel_handler_buy(dp)
cancel_handler_cripts_sell.register_handlers_cancel_handler_sell(dp)
buy_btc_chy.register_handlers_buy_btc_chy(dp)
sell_btc_chy.register_handlers_sell_btc_chy(dp)
buy_btc_usd.register_handlers_buy_btc_usd(dp)
sell_btc_usd.register_handlers_sell_btc_usd(dp)
buy_eth_chy.register_handlers_buy_eth_chy(dp)
sell_eth_chy.register_handlers_sell_eth_chy(dp)
buy_eth_usd.register_handlers_buy_eth_usd(dp)
sell_eth_usd.register_handlers_sell_eth_usd(dp)
info_profile_reply.register_handlers_info_reply(dp)
cripts_menu.register_handlers_cripts_list_menu(dp)
bonus_chy.register_handlers_bonus_chy(dp)
voice.register_handlers_voice(dp)
ls_message.register_handlers_ls_message(dp)
# <---------Новости----------->
news_cybersport.register_handlers_news(dp)
news_ixbt.register_handlers_news(dp)
#<---------------------------->
img_random.register_handlers_img_random(dp)
search_wiki.register_handlers_search_wiki(dp)
gif_random.register_handlers_gif_random(dp)
casino_spin.register_handlers_casino(dp)
client.register_handlers_client(dp)
help_kb.register_callback_query(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)
#<---------------------------------------------------------->

    

async def on_startup(_):
    me=await bot.get_me()
    print('\033[33m' +'[~] Bot '+'\033[0m'+'\033[39m' + me.first_name +'\033[0m' + '\033[33m'+' start!'+'\033[0m')
    await bot.send_message(chat_id=DEVELOPER,text='[~] Bot start!')
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
    loop.create_task(cripts_price_change.cripts_price_change())# тут в loop.create_task() указать название класса def для запустка цикла
    #<-------------------------------------------------->
    executor.start_polling(dp, skip_updates=True,on_startup=on_startup)