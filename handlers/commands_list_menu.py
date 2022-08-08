from aiogram import types, Dispatcher
from config import DEVELOPER
from create_bot import dp,bot



async def commands_list_menu(message: types.Message):
    if message.from_user.id != DEVELOPER:
        return
    await dp.bot.set_my_commands([
        types.BotCommand("help", "список команд"),
        types.BotCommand("mess","отправка сообщения по id"),
        types.BotCommand("info", "информация по свайпу"),
        types.BotCommand("profile","посмотреть профиль"),
        types.BotCommand("casino","казино(¥)"),
        types.BotCommand("bonus","бонус 1000-15000(¥) на счет"),
        types.BotCommand("wiki","поиск в википедии"),
        types.BotCommand("img","рандомная картинка по запросу"),
        types.BotCommand("gif","гифка рандомная"),
        types.BotCommand("voice","озвучка текста"),
        types.BotCommand("news","сайты с новостями"),
        types.BotCommand("cybersport","игровые новости"),
        types.BotCommand("ixbt","игровые новости"),
    ])
    await message.answer('Commands list add!')



# async def set_bot_commands(bot: Bot):
#     commands = [
#         BotCommand(command="start", description="Перезапустить казино"),
#         BotCommand(command="spin", description="Показать клавиатуру и сделать бросок"),
#         BotCommand(command="stop", description="Убрать клавиатуру"),
#         BotCommand(command="help", description="Справочная информация")
#     ]
#     await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())



def register_handlers_commands_list_menu(dp: Dispatcher):
    dp.register_message_handler(commands_list_menu,commands=['admin_commands_add'])
