import parser

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.markdown import text, bold, italic, code, pre
import config
import buttons
import utils
from parser import get_data, filter_response
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

bot = Bot(token=config.API)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

class Exchanging(StatesGroup):
    waiting_for_sum = State()
    waiting_for_name = State()
    waiting_for_first_name = State()
    waiting_for_second_name = State()
    op_type = None
    currency = None
    currency1 = None
    currency2 = None

@dp.callback_query_handler(lambda x: x.data == 'cancel')
async def usd(callback_query: types.CallbackQuery, state: FSMContext):
    Exchanging.op_type = None
    await state.finish()


@dp.callback_query_handler(lambda x: x.data == 'USD')
async def usd(callback_query: types.CallbackQuery):
    await Exchanging.waiting_for_name.set()
    await bot.send_message(chat_id=callback_query.from_user.id, text="Введите валюту")
    Exchanging.op_type = callback_query.data + "T"


@dp.callback_query_handler(lambda x: x.data == 'ETH', state='*')
async def eth(callback_query: types.CallbackQuery):
    await Exchanging.waiting_for_name.set()
    await bot.send_message(chat_id=callback_query.from_user.id, text="Введите валюту")
    Exchanging.op_type = callback_query.data


@dp.callback_query_handler(lambda x: x.data == 'BTC', state='*')
async def btc(callback_query: types.CallbackQuery):
    await Exchanging.waiting_for_name.set()
    await bot.send_message(chat_id=callback_query.from_user.id, text="Введите валюту")
    Exchanging.op_type = callback_query.data


@dp.callback_query_handler(lambda x: x.data == 'other', state='*')
async def other(callback_query: types.CallbackQuery):
    await Exchanging.waiting_for_first_name.set()
    await bot.send_message(chat_id=callback_query.from_user.id, text="Введите первую валюту")
    Exchanging.op_type = callback_query.data


@dp.message_handler(state=Exchanging.waiting_for_name)
async def read_name(message: types.Message,  state: FSMContext):
    name = message.text.upper().strip()
    Exchanging.currency = name
    available = parser.check_name(name)
    if not available:
        await message.reply("Такой валюты нет")
        Exchanging.op_type = None
        await state.finish()
    else:
        await message.reply("Введите сумму")
        await Exchanging.waiting_for_sum.set()


@dp.message_handler(state=Exchanging.waiting_for_first_name)
async def read_sum(message: types.Message,  state: FSMContext):
    name = message.text.upper().strip()
    Exchanging.currency = name
    available = parser.check_name(name)
    if not available:
        await message.reply("Такой валюты нет")
        Exchanging.op_type = None
        await state.finish()
    else:
        await message.reply("Введите вторую валюту")
        await Exchanging.waiting_for_second_name.set()
        Exchanging.currency1 = name


@dp.message_handler(state=Exchanging.waiting_for_second_name)
async def read_sum(message: types.Message,  state: FSMContext):
    name = message.text.upper().strip()
    Exchanging.currency = name
    available = parser.check_name(name)
    if not available and not name in ["USD", "BTC", "ETH"]:
        await message.reply("Такой валюты нет")
        Exchanging.op_type = None
        await state.finish()
    else:
        await message.reply("Введите сумму")
        await Exchanging.waiting_for_sum.set()
        Exchanging.currency2 = name


@dp.message_handler(state=Exchanging.waiting_for_sum)
async def read_sum(message: types.Message,  state: FSMContext):
    try:
        sum = int(message.text)
    except:
        await message.reply("Сумма должна быть числом", reply_markup=buttons.CANCEL)
    else:
        if Exchanging.op_type == "other":
            await bot.send_message(chat_id=message.chat.id,
                                   text=parser.convert(Exchanging.currency1, Exchanging.currency2, sum))
        else:
            await bot.send_message(chat_id=message.chat.id, text=parser.convert(Exchanging.op_type,
                                                                                  Exchanging.currency,sum))
        await state.finish()



@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):

    await bot.send_message(chat_id=message.chat.id, text="Привет!\nЯ бот для любителей криптовалюты. Надеюсь тебе\
                                                         понравится мой функционал.")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(text=text("Вот маленький список того что я умею делать:\n", "1. Я могу показать тебе топ-N криптовалют",
                            "\n2. Я могу конвертировать разные валюты", "\n3. Я могу показать наглядную диаграму",
                            "\n4. Я могу дать информацию о последних твитах Илона Маска, чтобы ты мог оценить их криптовалютные риски"))


@dp.message_handler(commands=['top'])
async def get_topN(message: types.Message):
    command = message.get_full_command()
    if len(command) == 1:
        await message.reply("Пожалуйста, укажи сколько коинов нужно показать")
        return
    N = command[1]
    try:
        N = int(N)
    except:
        await message.reply("В комманде нужно указать число")
        return
    if N <= 0:
        await message.reply("Не думаю, что я могу показать отрицательное число коинов")
        return
    all_data = get_data()
    needed_coins = filter_response(all_data, N)
    if len(needed_coins) < N:
        await bot.send_message(chat_id=message.chat.id, text= f"Удалось найти всего {len(needed_coins)} коинов")
    else:
        await bot.send_message(chat_id=message.chat.id, text= f"Вот {N} топовых коинов по отношению цены к BTC")
    await bot.send_message(chat_id=message.chat.id, text=utils.prettify_coins(needed_coins))


@dp.message_handler(commands=["exchange"])
async def exchange(message: types.Message):
    await message.reply("Что будем менять?", reply_markup=buttons.kb)


@dp.message_handler(commands=["news"])
async def exchange(message: types.Message):
    command = message.get_full_command()
    if len(command) == 1:
        await message.reply("Пожалуйста, укажи сколько статей нужно показать")
        return
    N = command[1]
    try:
        N = int(N)
    except:
        await message.reply("В комманде нужно указать число")
        return
    if N <= 0:
        await message.reply("Не думаю, что я могу показать отрицательное число статей")
        return
    articles = parser.parse_news(N)
    for article in articles:
        button = InlineKeyboardButton("Источник", url=article["link"])
        mk = InlineKeyboardMarkup().add(button)
        await bot.send_photo(chat_id=message.chat.id, photo=article["img"], caption=article["text"],
                             reply_markup=mk)


@dp.message_handler(commands=["check"])
async def exchange(message: types.Message):
    command = message.get_full_command()
    if len(command) == 1:
        await message.reply("Надо было указать еще и хэш транзакции")
        return
    await message.reply("Транзакция прошла успешно" if parser.check_transaction(hash) else "Транзакция не прошла")


@dp.message_handler(commands=["hist"])
async def exchange(message: types.Message):
    command = message.get_full_command()
    if len(command) == 1:
        await message.reply("Пожалуйста, укажи за сколько дней нужен график")
        return
    N = command[1]
    try:
        N = int(N)
    except:
        await message.reply("В комманде нужно указать число")
        return
    if int(N) <= 0:
        await message.reply("Не думаю, что я могу показать отрицательное число дней")
        return
    image = parser.get_historicalbtc(N)
    await bot.send_photo(chat_id=message.chat.id, photo=image)


if __name__ == "__main__":
    executor.start_polling(dp)
