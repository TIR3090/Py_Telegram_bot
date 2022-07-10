# import MySQLdb
# import mysql
# import aiomysql as sa
# from mysql.connector import connect,Error
# import MySQLdb as sq
import psycopg2 as sq
# import mysql.connector
# import sqlite3 as sq
from create_bot import dp,bot
from aiogram import types

def sql_start():
    global base, cur
    base = sq.connect(dbname='d9882ng2h7srs6', user='rixdvqeatezwpn',
                     password='60e4ac9ad7bcb8be1b8900f38fc0c70a52a69fb6dcdd59bf553c6262631f54a6', host='ec2-34-242-8-97.eu-west-1.compute.amazonaws.com')
    cur=base.cursor()
    if base:
        print('Data base connected OK!')
        cur.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
        cur.execute('CREATE TABLE IF NOT EXISTS profile(id TEXT PRIMARY KEY,avatar TEXT, nickname TEXT,balance DOUBLE PRECISION DEFAULT 0,bonus TIMESTAMP)')
        cur.execute('CREATE TABLE IF NOT EXISTS cripts(id TEXT PRIMARY KEY,cript TEXT,usd DOUBLE PRECISION,chy DOUBLE PRECISION)')
        base.commit()
        
async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (%s,%s,%s,%s)',tuple(data.values()))
        base.commit()

async def write_regist_prof(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO profile VALUES (%s,%s,%s,%s,%s)',tuple(data.values()))
        # print(tuple(data.values()))
        base.commit()

        
async def sql_read(message: types.Message):
    cur.execute('SELECT * FROM menu')
    for ret in cur.fetchall():
        await message.answer_photo(ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')
        
async  def read_regist_prof(message: types.Message):
    if message.from_user.id != 1133903696:
        cur.execute(f"SELECT * FROM profile WHERE id='{message.from_user.id}'")
        for test in cur.fetchall():
            await message.answer(f'[~~~Профиль~~~]\n\nid: {test[0]}\nНик: {test[2]}\n\n[~~~~~~~~~~~~]')
            # with open("encoding.jpg", "wb") as new_file:
            #     new_file.write(base64.decodebytes(test[1]))
    else:
        cur.execute('SELECT * FROM profile')
        for test in cur.fetchall():
            await message.answer(f'[~~~Профиль~~~]\n\nid: {test[0]}\nНик: {test[2]}\n\n[~~~~~~~~~~~~]')
            # with open("encoding.jpg", "wb") as new_file:
            #     new_file.write(base64.decodebytes(test[1]))
