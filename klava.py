
from aiogram.types import ReplyKeyboardMarkup,InlineKeyboardMarkup, InlineKeyboardButton

klava = ReplyKeyboardMarkup(resize_keyboard = True)
klava.row('> CREATE <')
klava.row('>LIST<', '>DELETE<', '>CORRECT<', '>HELP<')