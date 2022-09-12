import docx
from aiogram import types, Dispatcher
import aiosqlite as aoisq
from config import DEVELOPER


async def save_in_docx(message: types.Message):
    if message.from_user.id == DEVELOPER:
        global base, cur
        base =await aoisq.connect("data_base/data_casino_keeper.db")
        cur=await base.cursor()
        doc=docx.Document()
        await cur.execute(f"SELECT * FROM profile")
        for information in await cur.fetchall():
            doc.add_paragraph(f'[~~~Профиль~~~]\n\n'
                              f'🎫 id: {information[0]}\n'
                              f'avatar: {information[1]}\n'
                              f'avatar_info: {information[2]}\n'
                              f'first_name: {information[3]}\n'
                              f'💻 Ник: {information[4]}\n'
                              f'privilege: {information[5]}\n'
                              f'💵 $: {information[6]}\n'
                              f'💴 ¥: {information[7]}\n'
                              f'btc_usd: {information[8]}\n'
                              f'price_buy_btc_usd: {information[9]}\n'
                              f'btc_chy: {information[10]}\n'
                              f'price_buy_btc_chy: {information[11]}\n'
                              f'eth_usd: {information[12]}\n'
                              f'price_buy_eth_usd: {information[13]}\n'
                              f'eth_chy: {information[14]}\n'
                              f'price_buy_eth_chy: {information[15]}\n'
                              f'bonus_chy: {information[16]}\n'
                              f'level: {information[17]}\n'
                              f'exp: {information[18]}\n'
                              f'exp_next_level: {information[19]}\n'
                              f'health: {information[20]}\n'
                              f'armor: {information[21]}\n'
                              f'mage_resistance: {information[22]}\n'
                              f'phisic_resistance: {information[23]}\n'
                              f'right_hand: {information[24]}\n'
                              f'left_hand: {information[25]}\n'
                              f'inventory: {information[26]}\n\n'
                              f'[~~~~~~~~~~~~~]')
        doc.save('data.docx')
        await message.answer_document(open('data.docx', 'rb'))


def register_handlers_save_in_docx(dp: Dispatcher):
    dp.register_message_handler(save_in_docx, commands=['save_docx','сохранить_данные'])
