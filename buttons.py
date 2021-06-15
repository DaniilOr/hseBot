from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, \
                          ReplyKeyboardRemove


USD = InlineKeyboardButton('USD', callback_data='USD')
BTC = InlineKeyboardButton('BTC', callback_data='BTC')
ETH = InlineKeyboardButton('ETH', callback_data='ETH')
OTHER = InlineKeyboardButton('Другое', callback_data='other')

kb = InlineKeyboardMarkup(row_width=3, one_time_keyboard=True).add(BTC, USD, ETH)
kb.add(OTHER)

CANCEL =  InlineKeyboardButton('Отена', callback_data='cancel')