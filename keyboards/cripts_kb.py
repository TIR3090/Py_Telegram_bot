from aiogram.types import ReplyKeyboardMarkup,KeyboardButton, InlineKeyboardMarkup,InlineKeyboardButton



cripts_selection_sell=InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton(text='Bitcoin',callback_data='bitcoin_btc_sell'),InlineKeyboardButton(text='Ethereum',callback_data='ethereum_eth_sell'))
cripts_selection_buy=InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton(text='Bitcoin',callback_data='bitcoin_btc_buy'),InlineKeyboardButton(text='Ethereum',callback_data='ethereum_eth_buy'))
bitcoin_valuta_selection_sell=InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton(text='usd-$',callback_data='bitcoin_valuta_usd_sell'),InlineKeyboardButton(text='chy-¥',callback_data='bitcoin_valuta_chy_sell'))
bitcoin_valuta_selection_buy=InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton(text='usd-$',callback_data='bitcoin_valuta_usd_buy'),InlineKeyboardButton(text='chy-¥',callback_data='bitcoin_valuta_chy_buy'))
ethereum_valuta_selection_sell=InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton(text='usd-$',callback_data='ethereum_valuta_usd_sell'),InlineKeyboardButton(text='chy-¥',callback_data='ethereum_valuta_chy_sell'))
ethereum_valuta_selection_buy=InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton(text='usd-$',callback_data='ethereum_valuta_usd_buy'),InlineKeyboardButton(text='chy-¥',callback_data='ethereum_valuta_chy_buy'))




kb_buy=KeyboardButton('📥 купить')
kb_sell=KeyboardButton('📤 продать')
kb_curs=KeyboardButton('📊 курс крипты')
kb_back_menu=KeyboardButton('📜 меню')

kb_cripts_menu=ReplyKeyboardMarkup(resize_keyboard=True)
kb_cripts_menu.add(kb_buy,kb_sell).add(kb_curs).add(kb_back_menu)
