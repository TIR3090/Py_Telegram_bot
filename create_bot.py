from aiogram import Bot,    types
from aiogram.dispatcher import Dispatcher
from config import TOKEN,DEVELOPER
import os,json,string
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage=MemoryStorage()

bot= Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp=Dispatcher(bot, storage=storage)
