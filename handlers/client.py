from config import DEVELOPER
from handlers import registration
from aiogram import types, Dispatcher
from data_base import sqlite_db
from keyboards import admin_kb,client_kb,news_kb,help_kb
from aiogram.dispatcher.filters import Text



async def choosing_a_website_with_news(message: types.Message):
    await message.answer('Выберите сайт:',reply_markup=news_kb.news_selection)


    
# async def website(message: types.Message):
#     if registration.IsRegistration(message.from_user.id)==False:
#         await message.answer('/reg - Вначале зарегистрируйтесь!')
#         return
#     await message.answer('<a href="https://a62b-212-48-153-26.eu.ngrok.io">Редактировать профиль</a>',parse_mode=types.ParseMode.HTML)



async def test_menu_command(message: types.Message):
    await sqlite_db.sql_read(message)



async def Profile_smotr(message: types.Message):
    if await registration.IsRegistration(message.from_user.id)==False:
        await message.answer('/reg - Вначале зарегистрируйтесь!')
        return
    await sqlite_db.read_regist_prof(message)
    
    
    
async def menu(message: types.Message):
    if await registration.IsRegistration(message.from_user.id)==False:
        await message.answer('/reg - Вначале зарегистрируйтесь!')
        return
    await message.answer('Меню:',reply_markup=client_kb.kb_menu)


async def replace_bd_server(message: types.Message):
    if message.from_user.id == DEVELOPER:
        if document :=message.reply_to_message.document:
            await document.download(destination_file=f"data_base/data_casino_keeper.db")
        else:
            await message.answer('⚠️ ERROR WRONG <b>DataBase</b>!')

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(test_menu_command, commands=['menu','меню'])
    dp.register_message_handler(Profile_smotr, commands=['profile','профиль'])
    dp.register_message_handler(replace_bd_server,commands=['load_db','загрузить_бд'])
    dp.register_message_handler(choosing_a_website_with_news, commands=['news','новости'])
    dp.register_message_handler(choosing_a_website_with_news,Text(equals=['📰 news','📰 новости']))
    dp.register_message_handler(menu, commands=['menu','меню'])
    dp.register_message_handler(menu,Text(equals=['📜 menu','📜 меню']))
    # dp.register_message_handler(website, commands=['red','ред'])
