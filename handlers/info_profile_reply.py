from aiogram import types, Dispatcher
import psycopg2 as sq



async def info_reply(message: types.Message):
    global base, cur
    base = sq.connect(dbname='d9882ng2h7srs6',
                      user='rixdvqeatezwpn',
                      password='60e4ac9ad7bcb8be1b8900f38fc0c70a52a69fb6dcdd59bf553c6262631f54a6',
                      host='ec2-34-242-8-97.eu-west-1.compute.amazonaws.com')
    cur=base.cursor()
    if message.reply_to_message:
        cur.execute(f"SELECT * FROM profile WHERE id='{message.reply_to_message.from_user.id}'")
        for information in cur.fetchall():
            await message.answer_photo(information[2],
                                       f'[~~~Профиль~~~]\n\n'
                                       f'🎫 id: {information[0]}\n'
                                       f'💻 Ник: {information[4]}\n'
                                       f'💴 ¥: {information[6]}\n'
                                       f'💵 $: {information[7]}\n\n'
                                       f'[=====-Cripts-=====]\n\n'
                                       f'💼 ₿-¥: {"{:0.9f}".format(information[10])}\n'
                                       f'💼 ₿-$: {"{:0.9f}".format(information[8])}\n\n'
                                       f'💼 Ξ-¥: {"{:0.9f}".format(information[14])}\n'
                                       f'💼 Ξ-$: {"{:0.9f}".format(information[12])}\n\n'
                                       f'[~~~~~~~~~~~~~]')
    else:
        cur.execute(f"SELECT * FROM profile WHERE id='{message.from_user.id}'")
        for information in cur.fetchall():
            await message.answer_photo(information[2],
                                       f'[~~~Профиль~~~]\n\n'
                                       f'🎫 id: {information[0]}\n'
                                       f'💻 Ник: {information[4]}\n'
                                       f'💴 ¥: {information[6]}\n'
                                       f'💵 $: {information[7]}\n\n'
                                       f'[=====-Cripts-=====]\n\n'
                                       f'💼 ₿-¥: {"{:0.9f}".format(information[10])}\n'
                                       f'💼 ₿-$: {"{:0.9f}".format(information[8])}\n\n'
                                       f'💼 Ξ-¥: {"{:0.9f}".format(information[14])}\n'
                                       f'💼 Ξ-$: {"{:0.9f}".format(information[12])}\n\n'
                                       f'[~~~~~~~~~~~~~]')


def register_handlers_info_reply(dp: Dispatcher):
    dp.register_message_handler(info_reply, commands=['info','инфо'])
