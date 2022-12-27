from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import requests
from config import TOKEN
from config import JOKE_IP_TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    name = State()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Напиши /help, чтобы ознакомится со списком команд")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(
        "Напиши /joke и в ответ получишь шутку, напиши /photo и в ответ получишь фото кота, /count чтобы посчитать количество символов")


@dp.message_handler(commands=['joke'])
async def process_joke_command(message: types.Message):
    url = "https://dad-jokes.p.rapidapi.com/random/joke"

    headers = {
        "X-RapidAPI-Key": JOKE_IP_TOKEN,
        "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers)
    set_up = response.json()["body"][0]["setup"]
    punchline = response.json()["body"][0]["punchline"]
    await message.reply(set_up + '\n\n' + punchline)


@dp.message_handler(commands=['photo'])
async def process_photo_command(message: types.Message):
    url = "https://api.thecatapi.com/v1/images/search"
    caption = 'cute cat 🥰🥰🥰'
    response = requests.request("GET", url)
    await bot.send_photo(message.from_user.id, response.json()[0]['url'],
                         caption=caption,
                         reply_to_message_id=message.message_id)


@dp.message_handler(commands=['count'])
async def count(message: types.Message):
    await Form.name.set()
    await message.reply("Send text, or /cancel to interapt")


@dp.message_handler(state=Form.name, commands=['cancel'])
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Cancelled.')


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply(f"Sumbols with spaces - {len(message.text)}")


if __name__ == '__main__':
    executor.start_polling(dp)
