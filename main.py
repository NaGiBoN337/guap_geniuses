import logging
import os
from aiogram import Bot, Dispatcher, executor, types

# Объект бота
bot = Bot(token="5389746553:AAE6MsbpQ7nWYrMDWRfhQuhR06Z3EUefS0A")
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands="start")
async def start_answer(message: types.Message):
    await message.answer("Приветствую.\nЭтот бот умеет искать песню по ключевому слову, для работы с ним пришлите одно.")

@dp.message_handler(content_types=["text"])
async def process_voice_command(message: types.Message):
	listmusic = os.listdir('music')
	for i in listmusic:
		audio = open(r'music/' + i, 'rb')
		await bot.send_audio(message.chat.id, audio)
		audio.close()




if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
