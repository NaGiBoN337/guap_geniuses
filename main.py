import logging
from aiogram import Bot, Dispatcher, executor, types

# Объект бота
bot = Bot(token="5389746553:AAE6MsbpQ7nWYrMDWRfhQuhR06Z3EUefS0A")
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands="start")
async def start_answer(message: types.Message):
    await message.answer("Приветствую.\nЭтот бот умеет редактировать видео, для работы с ним пришлите одно.")

@dp.message_handler(content_types=["video"])
async def video_answer(message: types.Message):
	keyboard = types.InlineKeyboardMarkup()
	keyboard.add(types.InlineKeyboardButton(text="Добавить звук", callback_data="b1"))
	keyboard.add(types.InlineKeyboardButton(text="Убрать звук", callback_data="b2"))
	await message.answer("Ты прислал видео!\nЧто пожелаешь с ним сделать?",reply_markup=keyboard)
	await message.video.download() # вот строка, которая должна скачивать видос, каким образом это происходит я хз


@dp.callback_query_handler(text="b1") # Добавить звук
async def b1(call: types.CallbackQuery):
	keyboard = types.InlineKeyboardMarkup()
	keyboard.add(types.InlineKeyboardButton(text="Я пришлю файл", callback_data="b11"))
	keyboard.add(types.InlineKeyboardButton(text="Я пришлю голосовое сообщение", callback_data="b12"))
	#keyboard.add(types.InlineKeyboardButton(text="Я хочу воспользоваться встроенным поиском", callback_data="b13"))
	await call.message.answer("Каким способом вы хотите прислать аудио?",reply_markup=keyboard)
	

@dp.callback_query_handler(text="b2") # Убрать звук
async def b2(message: types.Message):
	# убрать звук()
    #await bot.send_video(/vi\)
    await message.answer("звук убран")


@dp.callback_query_handler(text="b11")
async def b11(call: types.CallbackQuery):
    await call.message.answer('пришлите файл')


@dp.callback_query_handler(text="b12")
async def b12(call: types.CallbackQuery):
	await call.message.answer('пришлите голосовое сообщение')


@dp.message_handler(content_types=["audio"])
async def audio_answer(message):
	await message.audio.download()
	#await bot.send_message(message.chat.id, "Аудио.")
	#await bot.send_video(/vi\)

@dp.message_handler(content_types=["voice"])
async def voice_answer(message):
	await message.voice.download()
	#await bot.send_message(message.chat.id, "voice.")
	#await bot.send_video(/vi\)





if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
