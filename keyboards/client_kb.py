from aiogram.types import ReplyKeyboardMarkup,KeyboardButton, InlineKeyboardMarkup,InlineKeyboardButton

kb_casino=KeyboardButton('🎰 казино')
kb_news=KeyboardButton('📰 новости')
kb_cripts=KeyboardButton('📈 криптовалюта')

kb_menu=ReplyKeyboardMarkup(resize_keyboard=True)
kb_menu.add(kb_casino).add(kb_news).add(kb_cripts)

