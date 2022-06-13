import telebot;
import os
from parsing import main_down_music
from keybord import *

from logic import *

bot = telebot.TeleBot("5389746553:AAE6MsbpQ7nWYrMDWRfhQuhR06Z3EUefS0A");
bot.remove_webhook()


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'Приветствую.\nЭтот бот умеет искать песню по ключевому слову, для работы с ним пришлите одно.\nтак же в кнопках вы можите выбрать максимальное колличество присылаемых песен\n команда для смены количества песен - /change')


@bot.message_handler(commands=['change'])
def start_message(message):
    bot.send_message(message.chat.id, 'сменить количество', reply_markup=numbers_music)


@bot.message_handler(content_types=["text"])
def any_msg(message):
    numbers_users_m = int(load_users_info(str(message.from_user.id)))

    if main_down_music(message.text) == 1:
        bot.send_message(message.from_user.id, "Уточните запрос")
    else:
        listmusic = os.listdir('music')
        for i in listmusic:
            numbers_users_m -= 1
            audio = open(r'music/' + i, 'rb')
            bot.send_audio(message.from_user.id, audio)
            audio.close()
            if numbers_users_m <= 0:
                break


@bot.callback_query_handler(func=lambda call: True)
def i_can(call):
    if call.message:

        if call.data == "1":
            bot.send_message(call.from_user.id, "Окей, песен будет 1, если захотите изменить напишите /change")
        if call.data == "3":
            bot.send_message(call.from_user.id, "Окей, песен будет 3, если захотите изменить напишите /change")
        if call.data == "5":
            bot.send_message(call.from_user.id, "Окей, песен будет 5, если захотите изменить напишите /change")
        if call.data == "10":
            bot.send_message(call.from_user.id, "Окей, песен будет 10, если захотите изменить напишите /change")

        tm = load_users()
        tm[str(call.from_user.id)] = call.data

        capitals_json = json.dumps(tm)
        with open("users.json", "w") as my_file:
            my_file.write(capitals_json)


bot.polling(none_stop=True, interval=0)
