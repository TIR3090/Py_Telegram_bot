from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_load=KeyboardButton('/загрузить')
button_delete=KeyboardButton('/удалить')

kb_admin_chy_add=KeyboardButton('/add_chy_developer')
kb_admin_save_db=KeyboardButton('/save_docx')
kb_admin_load_db=KeyboardButton('/load_db')



kb_admin_tools=ReplyKeyboardMarkup(resize_keyboard=True)
kb_admin_tools.add(kb_admin_chy_add)


button_case_admin=ReplyKeyboardMarkup(resize_keyboard=True).add(button_load)\
    .add(button_delete)