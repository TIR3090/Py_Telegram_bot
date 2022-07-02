﻿from aiogram import Dispatcher,types
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton, InlineKeyboardMarkup,InlineKeyboardButton

b1=KeyboardButton('🎰')
b2=KeyboardButton('📜')
b3=KeyboardButton('📈')

kb_client=ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b1).add(b2).add(b3)


inkb_help_list_1=InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton(text='<-',callback_data='<-help_list2_left'),InlineKeyboardButton(text='Команды @',callback_data='help_list_midl'),InlineKeyboardButton(text='->',callback_data='help_list2_right->'))
inkib_help_list_midl=InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='YouTube',switch_inline_query_current_chat=''),InlineKeyboardButton(text='Tenor gif',switch_inline_query_current_chat='gif '),InlineKeyboardButton(text='вернуться',callback_data='back_help_list_1'))
inkb_help_list_2=InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton(text='<-',callback_data='<-help_list1_left'),InlineKeyboardButton(text='Команды @',callback_data='help_list_midl'),InlineKeyboardButton(text='->',callback_data='help_list1_right->'))

help_1=('<b>/help</b> - список команд\n' \
        '<b>/wiki</b> - поиск в википедии\n' \
        '<b>/img</b> - рандомная картинка по запросу\n' \
        '<b>/gif</b> - гифка рандомная\n' \
        '<b>/voice</b> - озвучка текста ')


help_2=('<b>/reg</b> - регистрация\n' \
        '<b>/profs</b> - регистрация\n' \
        '<b>/casino</b> - казино\n' \
        '<b>/balance</b> - баланс\n' \
        '<b>/cybersport</b> - игровые новости')

help_at_sign =('<b>@C_K_1_bot</b> - поиск в YouTube\n' \
               '<b>@C_K_1_bot gif</b> - поиск в gif Tenor')


async def help_list1_left(callback: types.CallbackQuery):
    await callback.message.edit_text(help_2,reply_markup=inkb_help_list_2)
    await callback.answer()

async def help_list1_right(callback: types.CallbackQuery):
    await callback.message.edit_text(help_2,reply_markup=inkb_help_list_2)
    await callback.answer()

async def help_list2_left(callback: types.CallbackQuery):
    await callback.message.edit_text(help_1,reply_markup=inkb_help_list_1)
    await callback.answer()


async def help_list2_right(callback: types.CallbackQuery):
    await callback.message.edit_text(help_1,reply_markup=inkb_help_list_1)
    await callback.answer()

async def help_list_at_sign_back(callback: types.CallbackQuery):
    await callback.message.edit_text(help_1,reply_markup=inkb_help_list_1)
    await callback.answer()


async def help_list_at_sign(callback: types.CallbackQuery):
    await callback.message.edit_text(help_at_sign,reply_markup=inkib_help_list_midl)
    await callback.answer()

def register_callback_query(dp: Dispatcher):
    dp.register_callback_query_handler(help_list1_right,text='help_list2_right->')
    dp.register_callback_query_handler(help_list_at_sign,text='help_list_midl')
    dp.register_callback_query_handler(help_list1_left,text='<-help_list2_left')
    dp.register_callback_query_handler(help_list2_right,text='help_list1_right->')
    dp.register_callback_query_handler(help_list_at_sign_back,text='back_help_list_1')
    dp.register_callback_query_handler(help_list2_left,text='<-help_list1_left')
