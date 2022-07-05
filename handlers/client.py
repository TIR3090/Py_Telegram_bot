import datetime
import random
import requests
from handlers import registration
import wikipedia
import psycopg2 as sq
from aiogram import types, Dispatcher
from bs4 import BeautifulSoup
from translate import Translator
from create_bot import dp,bot
from data_base import sqlite_db
from keyboards import admin_kb,client_kb
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher.filters import Text
from handlers import news_cybersport,news_ixbt
import base64


async def bonus(message: types.Message):
    if registration.IsRegistration(message.from_user.id)==False:
        await message.answer('/reg - Вначале зарегистрируйтесь!')
        return 
    global base, cur
    base = sq.connect(dbname='d9882ng2h7srs6', user='rixdvqeatezwpn',
                      password='60e4ac9ad7bcb8be1b8900f38fc0c70a52a69fb6dcdd59bf553c6262631f54a6', host='ec2-34-242-8-97.eu-west-1.compute.amazonaws.com')
    cur=base.cursor()
    cur.execute(f"SELECT balance,bonus FROM profile WHERE id='{message.from_user.id}'")
    for inform_v_bd in cur.fetchall():
        if datetime.datetime.now()<inform_v_bd[1]:
            ost_time_bonus=inform_v_bd[1].replace(microsecond=0)-datetime.datetime.now().replace(microsecond=0)
            await message.answer(f'Бонус будет доступен через:\n⌚ {ost_time_bonus}')
        else:
            bonus_nachisl=random.uniform(1000,15000)
            balance_v_bd=int(inform_v_bd[0])+round(bonus_nachisl,3)
            bonus_poluch = datetime.datetime.now() + datetime.timedelta(minutes=90)
            cur.execute(f"UPDATE profile SET balance='{balance_v_bd}',bonus='{bonus_poluch}' WHERE id='{message.from_user.id}'")
            base.commit()
            await message.answer(f"Бонус получен!\n💸 {round(bonus_nachisl,3)} ¥\n⏱ {bonus_poluch.strftime('%H:%M')}")

async def commands_list_menu(message: types.Message):
    if message.from_user.id != 1133903696:
        return
    await dp.bot.set_my_commands([
        types.BotCommand("help", "список команд"),
        types.BotCommand("wiki","поиск в википедии"),
        types.BotCommand("news","сайты с новостями"),
        types.BotCommand("img","рандомная картинка по запросу"),
        types.BotCommand("gif","гифка рандомная"),
        types.BotCommand("voice","озвучка текста"),
        types.BotCommand("reg", "регистрация"),
        types.BotCommand("profs","регистрация"),
        types.BotCommand("casino","казино"),
        types.BotCommand("bonus","бонус 1000 на счет"),
        types.BotCommand("cybersport","игровые новости"),
        types.BotCommand("ixbt","игровые новости"),
    ])
    await message.answer('Commands list add!')

async def help_command(message: types.Message):
    help=('<code>1 страница:</code>\n'\
          '<b>/help</b> - список команд\n'\
         '<b>/wiki</b> - поиск в википедии\n' \
         '<b>/img</b> - рандомная картинка по запросу\n' \
         '<b>/gif</b> - гифка рандомная\n' \
         '<b>/voice</b> - озвучка текста')
    await message.answer(help,reply_markup=client_kb.inkb_help_list_1)
    await message.answer('Меню:',reply_markup=client_kb.kb_menu)

async def choosing_a_website_with_news(message: types.Message):
    await message.answer('Выберите сайт:',reply_markup=client_kb.news_selection)
    
    
    
async def website_news_cybersports_games(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(f'<b>Сybersport</b>\nВыберите кол-во новостей:',reply_markup=client_kb.news_cybersports_games_kolv)
    await callback.answer()



async def website_news_ixbt_games(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(f'<b>ixbt</b>\nВыберите кол-во новостей:',reply_markup=client_kb.news_ixbt_games_kolv)
    await callback.answer()


class FSMregistration(StatesGroup):
    id=State()
    photo=State()
    nickname=State()
    balance=State()
    bonus=State()


async  def cancel_handler(message: types.Message,state:FSMContext):
    current_state=await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('❌ Регистрация отменена!')


async def Start_registration(message: types.Message):
    if registration.IsRegistration(message.from_user.id)==True:
        await message.answer('Вы уже зарегистрированы!')
        return
    await FSMregistration.photo.set()
    await message.reply('/cancel- отмена\nЗагрузи фото для профиля:') 


async def reg_Photo_profile_load_photo(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['id']=message.from_user.id
        await message.photo[-1].download(destination_file=f"profiles_photos/encoding.jpg")
        with open(f"profiles_photos/encoding.jpg", "rb") as image_file:
            tmp = base64.b64encode(image_file.read()).decode()
        data['photo']= str(tmp)
    await FSMregistration.next()
    await message.reply('/cancel- отмена\nВведите ник:')

async def reg_Nickname_profile(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['nickname']=message.text
        data['balance']=0
        data['bonus']=datetime.datetime.now()
    await message.answer("✅ Регистрация прошла успешно!",reply_markup=client_kb.kb_menu)

    await sqlite_db.write_regist_prof(state)

    await state.finish()

# async def set_bot_commands(bot: Bot):
#     commands = [
#         BotCommand(command="start", description="Перезапустить казино"),
#         BotCommand(command="spin", description="Показать клавиатуру и сделать бросок"),
#         BotCommand(command="stop", description="Убрать клавиатуру"),
#         BotCommand(command="help", description="Справочная информация")
#     ]
#     await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())

# @dp.message_handler(commands=['start','help'])
async def commands_start(message: types.Message):
    # try:
    # await message.reply('Тест прошел успешно!', reply_markup=kb_client)
    await message.reply(f'Тест прошел успешно!\nid твой: {message.from_user.id} \n id chat: {message.chat.id}', reply_markup=admin_kb.button_case_admin)   
    #     await message.delete()
    # except:
    #   await message.reply('Напиши боту!:\n@Casino_keeper_1_bot')

# async def registration(message: types.Message):
#     await message.answer("✅ Регистрация прошла успешно!")
    
async def website(message: types.Message):
    if registration.IsRegistration(message.from_user.id)==False:
        await message.answer('/reg - Вначале зарегистрируйтесь!')
        return
    await message.answer('<a href="https://a62b-212-48-153-26.eu.ngrok.io">Редактировать профиль</a>',parse_mode=types.ParseMode.HTML)
    
async def test_menu_command(message: types.Message):
    await sqlite_db.sql_read(message)

async def Profile_smotr(message: types.Message):
    if registration.IsRegistration(message.from_user.id)==False:
        await message.answer('/reg - Вначале зарегистрируйтесь!')
        return
    await sqlite_db.read_regist_prof(message)



# async  def dice_casino(message: types.Message):
#     if registration.IsRegistration(message.from_user.id)==False:
#         await message.answer('/reg - Вначале зарегистрируйтесь!')
#         return
#     slot_machine_value = [
#         ["bar | bar | bar"],
#         ["grape | bar | bar"],
#         ["lemon | bar | bar"],
#         ["seven | bar | bar"],
#         ["bar | grape | bar"],
#         ["grape | grape | bar"],
#         ["lemon | grape | bar"],
#         ["seven | grape | bar"],
#         ["bar | lemon | bar"],
#         ["grape | lemon | bar"],
#         ["lemon | lemon | bar"],
#         ["seven | lemon | bar"],
#         ["bar | seven | bar"],
#         ["grape | seven | bar"],
#         ["lemon | seven | bar"],
#         ["seven | seven | bar"],
#         ["bar | bar | grape"],
#         ["grape | bar | grape"],
#         ["lemon | bar | grape"],
#         ["seven | bar | grape"],
#         ["bar | grape | grape"],
#         ["grape | grape | grape"],
#         ["lemon | grape | grape"],
#         ["seven | grape | grape"],
#         ["bar | lemon | grape"],
#         ["grape | lemon | grape"],
#         ["lemon | lemon | grape"],
#         ["seven | lemon | grape"],
#         ["bar | seven | grape"],
#         ["grape | seven | grape"],
#         ["lemon | seven | grape"],
#         ["seven | seven | grape"],
#         ["bar | bar | lemon"],
#         ["grape | bar | lemon"],
#         ["lemon | bar | lemon"],
#         ["seven | bar | lemon"],
#         ["bar | grape | lemon"],
#         ["grape | grape | lemon"],
#         ["lemon | grape | lemon"],
#         ["seven | grape | lemon"],
#         ["bar | lemon | lemon"],
#         ["grape | lemon | lemon"],
#         ["lemon | lemon | lemon"],
#         ["seven | lemon | lemon"],
#         ["bar | seven | lemon"],
#         ["grape | seven | lemon"],
#         ["lemon | seven | lemon"],
#         ["seven | seven | lemon"],
#         ["bar | bar | seven"],
#         ["grape | bar | seven"],
#         ["lemon | bar | seven"],
#         ["seven | bar | seven"],
#         ["bar | grape | seven"],
#         ["grape | grape | seven"],
#         ["lemon | grape | seven"],
#         ["seven | grape | seven"],
#         ["bar | lemon | seven"],
#         ["grape | lemon | seven"],
#         ["lemon | lemon | seven"],
#         ["seven | lemon | seven"],
#         ["bar | seven | seven"],
#         ["grape | seven | seven"],
#         ["lemon | seven | seven"],
#         ["seven | seven | seven"],
#     ]
#     casino = await message.answer_dice('🎰')
#     print(slot_machine_value[casino.dice.value-1])
#     await asyncio.sleep(2)
#     await message.reply(slot_machine_value[casino.dice.value-1])
    
#<!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!>
    #Переделать систему под State-машину
async  def inform_wiki_pedia(message: types.Message):
    if registration.IsRegistration(message.from_user.id)==False:
        await message.answer('/reg - Вначале зарегистрируйтесь!')
        return
    try:
        wikipedia.set_lang("ru")
        wiki_post=message.text[6:]
        push_wiki=wikipedia.summary(f"{wiki_post}")
        # push_wiki_all_info= wikipedia.page(f"{wiki_post}").content
        # push_wiki_all_info1= wikipedia.search(f"{wiki_post}")
        # await message.reply(push_wiki_all_info1)
        # print(push_wiki_all_info)
        await message.reply(push_wiki)
    except:
        try:
            push_wiki_search= wikipedia.search(f"{wiki_post}")
            await message.reply(push_wiki_search)
            await message.reply('/wiki [Что хотите найти]\n/вики [Что хотите найти]')
        except:
            await message.reply('/wiki [Что хотите найти]\n/вики [Что хотите найти]')
async def GIF_tenor(message: types.Message):
    try:
        trans=Translator(from_lang='ru',to_lang='en')
        gifki_zapr=message.text[5:]
        # en_form=trans.translate(gifki_zapr)
        tenor_api_key='AIzaSyBOcqMmqBT9JD1sLs5y7K-9Q6KRbMcci3g'
        ckey='py teleg bot'
        # response = requests.get(f"https://tenor.com/search/{gifki_zapr}-gifs")
        # soup=BeautifulSoup(response.text,features="html.parser")
        gifs = []
        # soup.findAll()
        # for gif in soup.findAll('img'):
        #     gifs.append(gif.get('src'))
        response = requests.get(f"https://tenor.googleapis.com/v2/search?q={gifki_zapr}&key={tenor_api_key}&client_key={ckey}&limit=100000")
        for view in response.json()['results']:
            gifs.append(view['url'])
        await message.answer_animation(random.choice(gifs))
    except:
        await message.reply('/gif [что ищите]\n/гиф [что ищите]')

async def image_yandex(message: types.Message):
    try:  
        photo=message.text[5:]
        response = requests.get(f"https://yandex.ru/images/search?text={photo}&from=tabbar")
        soup = BeautifulSoup(response.text, features="html.parser")
        images = []
        for img in soup.findAll('img'):
            images.append(img.get('src'))
        await message.answer_photo("https:"+random.choice(images))
    except:
        await message.reply('/img [что ищите]\n/имг [что ищите]')
#<---------------------------------->  
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(Start_registration, commands=['start','старт','reg','рег'],start=None)
    dp.register_message_handler(cancel_handler, state="*", commands =['отмена','cancel'])
    dp.register_message_handler(cancel_handler,Text(equals=['отмена','cancel'], ignore_case=True),state="*")
    dp.register_message_handler(reg_Photo_profile_load_photo, content_types=['photo'], state = FSMregistration.photo)
    dp.register_message_handler(reg_Nickname_profile, state = FSMregistration.nickname)
    # dp.register_message_handler(commands_start,commands=['start','help','старт','помощь'])
    dp.register_message_handler(help_command, commands=['help','помощь'])
    dp.register_message_handler(test_menu_command, commands=['menu','меню'])
    dp.register_message_handler(Profile_smotr, commands=['profs','проф'])
    dp.register_message_handler(choosing_a_website_with_news, commands=['news','новости'])
    dp.register_message_handler(choosing_a_website_with_news,Text(equals=['📰 news','📰 новости']))
    dp.register_message_handler(website, commands=['red','ред'])
    # dp.register_message_handler(dice_casino, commands=['casino','казино'])
    dp.register_message_handler(commands_list_menu,commands=['admin_commands_add'])
    # <---------Новости----------->
    dp.register_callback_query_handler(website_news_cybersports_games,text='cybersports_news')
    dp.register_callback_query_handler(website_news_ixbt_games,text='ixbt_news')
    #<---------------------------->
    # <-----тестовая команда------>
    dp.register_message_handler(inform_wiki_pedia, commands=['wiki','вики'])
    dp.register_message_handler(image_yandex, commands=['img','имг'])
    dp.register_message_handler(GIF_tenor, commands=['gif','гиф'])
    #<---------------------------->
    dp.register_message_handler(bonus, commands=['bonus','бонус'])
# dp.register_message_handler()