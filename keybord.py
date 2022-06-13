from telebot import types
import telebot;


numbers_music = types.InlineKeyboardMarkup()
numbers_music.add(types.InlineKeyboardButton(text="1", callback_data="1"))
numbers_music.add(types.InlineKeyboardButton(text="3", callback_data="3"))
numbers_music.add(types.InlineKeyboardButton(text="5", callback_data="5"))