# import MySQLdb
# import mysql
# import aiomysql as sa
# from mysql.connector import connect,Error
# import MySQLdb as sq
# import psycopg2 as sq
# import mysql.connector
# import sqlite3 as sq
from config import DEVELOPER
from create_bot import dp,bot
from aiogram import types
import aiosqlite as aoisq



async def sql_start():
    global base, cur
    # base = sq.connect(dbname='d9882ng2h7srs6',
    #                   user='rixdvqeatezwpn',
    #                   password='60e4ac9ad7bcb8be1b8900f38fc0c70a52a69fb6dcdd59bf553c6262631f54a6',
    #                   host='ec2-34-242-8-97.eu-west-1.compute.amazonaws.com')
    # cur=base.cursor()
    base =await aoisq.connect("data_base/data_casino_keeper.db")
    cur=await base.cursor()
    if base:
        print('Data base connected OK!')
        await cur.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT,'
                    ' name TEXT PRIMARY KEY,'
                    ' description TEXT,'
                    ' price TEXT)')


        await cur.execute('CREATE TABLE IF NOT EXISTS profile(id TEXT PRIMARY KEY,'
                    'avatar TEXT,'
                    'avatar_info TEXT,'
                    'first_name TEXT,'
                    'nickname TEXT,'
                    'privilege TEXT DEFAULT 0,'
                    'balance_usd DOUBLE PRECISION DEFAULT 0,'
                    'balance_chy DOUBLE PRECISION DEFAULT 0,'
                    'btc_usd DOUBLE PRECISION DEFAULT 0,'
                    'price_buy_btc_usd DOUBLE PRECISION DEFAULT 0,'
                    'btc_chy DOUBLE PRECISION DEFAULT 0,'
                    'price_buy_btc_chy DOUBLE PRECISION DEFAULT 0,'
                    'eth_usd DOUBLE PRECISION DEFAULT 0,'
                    'price_buy_eth_usd DOUBLE PRECISION DEFAULT 0,'
                    'eth_chy DOUBLE PRECISION DEFAULT 0,'
                    'price_buy_eth_chy DOUBLE PRECISION DEFAULT 0,'
                    'bonus_chy TIMESTAMP,'
                    'level INTEGER DEFAULT 0,'
                    'exp DOUBLE PRECISION DEFAULT 0,'
                    'exp_next_level DOUBLE PRECISION DEFAULT 0,'
                    'health DOUBLE PRECISION DEFAULT 0,'
                    'armor DOUBLE PRECISION DEFAULT 0,'
                    'mage_resistance DOUBLE PRECISION DEFAULT 0,'
                    'phisic_resistance DOUBLE PRECISION DEFAULT 0,'
                    'right_hand DOUBLE PRECISION DEFAULT 0,'
                    'left_hand DOUBLE PRECISION DEFAULT 0,'
                    'inventory TEXT)')



        await cur.execute('CREATE TABLE IF NOT EXISTS crips(id TEXT PRIMARY KEY,'
                    'name TEXT,'
                    'exp TEXT DEFAULT 0,'
                    'level_min DOUBLE PRECISION DEFAULT 0,'
                    'level_max DOUBLE PRECISION DEFAULT 0,'
                    'damage_min DOUBLE PRECISION DEFAULT 0,'
                    'damage_max DOUBLE PRECISION DEFAULT 0,'
                    'crit_chance DOUBLE PRECISION DEFAULT 0,'
                    'crit_damage DOUBLE PRECISION DEFAULT 0,'
                    'health DOUBLE PRECISION DEFAULT 0,'
                    'armor DOUBLE PRECISION DEFAULT 0,'
                    'mage_resistance DOUBLE PRECISION DEFAULT 0,'
                    'phisic_resistance DOUBLE PRECISION DEFAULT 0,'
                    'chy DOUBLE PRECISION DEFAULT 0,'
                    'usd DOUBLE PRECISION DEFAULT 0)')


        await cur.execute('CREATE TABLE IF NOT EXISTS cripts(id TEXT PRIMARY KEY,'
                    'cript TEXT,'
                    'usd DOUBLE PRECISION,'
                    'chy DOUBLE PRECISION)')
        await base.commit()
        
async def sql_add_command(state):
    async with state.proxy() as data:
        await cur.execute('INSERT INTO menu VALUES (%s,%s,%s,%s)',tuple(data.values()))
        await base.commit()

async def write_regist_prof(state):
    async with state.proxy() as data:
        await cur.execute('INSERT INTO profile(id,avatar,avatar_info,first_name,nickname,bonus_chy) VALUES (?,?,?,?,?,?)',tuple(data.values()))
        # print(tuple(data.values()))
        await base.commit()

        
async def sql_read(message: types.Message):
    await cur.execute('SELECT * FROM menu')
    for ret in await cur.fetchall():
        await message.answer_photo(ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')
        
async  def read_regist_prof(message: types.Message):
    if message.from_user.id != DEVELOPER:
        await cur.execute(f"SELECT * FROM profile WHERE id='{message.from_user.id}'")
        for information in await cur.fetchall():
            await message.answer_photo(information[2],
                                 f'[~~~Профиль~~~]\n\n'
                                 f'🎫 id: {information[0]}\n'
                                 f'💻 Ник: {information[4]}\n'
                                 f'💴 ¥: {information[7]}\n'
                                 f'💵 $: {information[6]}\n\n'
                                 f'[=====-Cripts-=====]\n\n'
                                 f'💼 ₿-¥: {"{:0.9f}".format(information[10])}\n'
                                 f'💼 ₿-$: {"{:0.9f}".format(information[8])}\n\n'
                                 f'💼 Ξ-¥: {"{:0.9f}".format(information[14])}\n'
                                 f'💼 Ξ-$: {"{:0.9f}".format(information[12])}\n\n'
                                 f'[~~~~~~~~~~~~~]')
            # with open("encoding.jpg", "wb") as new_file:
            #     new_file.write(base64.decodebytes(test[1]))
    else:
        await cur.execute('SELECT * FROM profile')
        for information in await cur.fetchall():
            await message.answer_photo(information[2],
                                 f'[~~~Профиль~~~]\n\n'
                                 f'🎫 id: {information[0]}\n'
                                 f'💻 Ник: {information[4]}\n'
                                 f'💴 ¥: {information[7]}\n'
                                 f'💵 $: {information[6]}\n\n'
                                 f'[=====-Cripts-=====]\n\n'
                                 f'💼 ₿-¥: {"{:0.9f}".format(information[10])}\n'
                                 f'💼 ₿-$: {"{:0.9f}".format(information[8])}\n\n'
                                 f'💼 Ξ-¥: {"{:0.9f}".format(information[14])}\n'
                                 f'💼 Ξ-$: {"{:0.9f}".format(information[12])}\n\n'
                                 f'[~~~~~~~~~~~~~]')
            # with open("encoding.jpg", "wb") as new_file:
            #     new_file.write(base64.decodebytes(test[1]))
