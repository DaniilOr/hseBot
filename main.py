import telebot
import parse
import json
import stats
import utils
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)
from telebot import types
from typing import Any

UPLOAD, POSTPROCESSING = range(2)

API_TOKEN = "5099641786:AAH6fMeMuWDQbu7n5tKlXq_v2iXVYscwlpE"

bot = telebot.TeleBot(API_TOKEN, parse_mode=None)


def send_welcome(update: {types.Message}, _: Any) -> int:
    """
    Welcomes the user. Returns the next step

    :param update: {message}
    :param _: Any
    """
    update.message.reply_text("Привет! Я - бот для небольшой помощи с финансовыми расчетами.\nЯ могу дать отчет по .csv файлам с data.nasdaq.com\n\
Отправь max/min/avg/med/std и можешь добавить временые рамки в формате \"FROM TO\", где FROM и TO - даты в формате YYYY-MM-DD. Также можно удалить файлы командой delete или попросить меня начертить график командой plot")
    return UPLOAD


def handle_docs(update: {types.Message}, _:Any) -> int:
    """
    This function uploads user date.

    :param updated: Message - updated wrapper of message
    """
    file_info = bot.get_file(update.message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    if update.message.document.mime_type == "application/json":
        csv_file = parse.json_to_csv(downloaded_file, update.message.from_user.id)
    else:
        csv_file = parse.save_csv(downloaded_file, update.message.from_user.id)
    if csv_file is None:
        update.message.reply_text("Что-то пошло не так. Это точно верный файл?")
        return UPLOAD
    else:
        update.message.reply_text("Файл сохранен, теперь можно получать из него информацию")
    return POSTPROCESSING


def cancel(update: {types.Message}, _:Any)->int:
    """
    This function stops conversation.

    :param updated: Message - updated wrapper of message
    """
    update.message.reply_text(
        'Мое дело предложить - Ваше отказаться'
        ' Будет нужна помощь - пиши.',
    )
    return ConversationHandler.END


def delete(update: {types.Message}, _:Any)->int:
    """
    This function deletes user files from the system.

    :param updated: Message - updated wrapper of message
    """
    res = utils.delete_file(update.message.from_user.id)
    if res:
        update.message.reply_text(
            'Ваши данные удалены. Спасибо за использование бота!',
        )
    else:
        update.message.reply_text(
            'А удалять-то  нечего.',
        )
    return ConversationHandler.END


def find_min(updated: {types.Message}, _:Any)->int:
    """
    This function sends min to the user.

    :param updated: Message - updated wrapper of message
    """
    if len(updated.message.text.split()) == 1:
        updated.message.reply_text("Считаем минимум на всем диапазоне данных")
        res = stats.calculate_min(updated.message.from_user.id)
    elif len(updated.message.text.split()) == 3 and parse.is_date(updated.message.text.split()[1]) and \
            parse.is_date(updated.message.text.split()[2]):
        updated.message.reply_text("Считаем минимум на диапазоне между указанными датами")
        _, start, end = updated.message.text.split()
        res = stats.calculate_min(updated.message.from_user.id, start, end)
    else:
        updated.message.reply_text("Введите просто /min или /min с указанием двух дат (Y-m-d)")
        return POSTPROCESSING
    if res is None:
        updated.message.reply_text("Вы точно ввели даты в формате Y-m-d? А файл точно не удаляли?")
        return POSTPROCESSING
    updated.message.reply_text(f"Min = {res}")
    return POSTPROCESSING


def find_max(updated: {types.Message}, _:Any)->int:
    """
    This function sends max to the user.

    :param updated: Message - updated wrapper of message
    """
    if len(updated.message.text.split()) == 1:
        updated.message.reply_text("Считаем максимум на всем диапазоне данных")
        res = stats.calculate_max(updated.message.from_user.id)
    elif len(updated.message.text.split()) == 3 and parse.is_date(updated.message.text.split()[1]) and \
            parse.is_date(updated.message.text.split()[2]):
        updated.message.reply_text("Считаем максимум на диапазоне между указанными датами")
        _, start, end = updated.message.text.split()
        res = stats.calculate_max(updated.message.from_user.id, start, end)
    else:
        updated.message.reply_text("Введите просто /max или /max с указанием двух дат (Y-m-d)")
        return POSTPROCESSING
    if res is None:
        updated.message.reply_text("Вы точно ввели даты в формате Y-m-d? А файл точно не удаляли?")
        return POSTPROCESSING
    updated.message.reply_text(f"Max = {res}")
    return POSTPROCESSING


def find_avg(updated: {types.Message}, _:Any)->int:
    """
    This function sends mean to the user.

    :param updated: Message - updated wrapper of message
    """
    if len(updated.message.text.split()) == 1:
        updated.message.reply_text("Считаем среднее на всем диапазоне данных")
        res = stats.calculate_avg(updated.message.from_user.id)
    elif len(updated.message.text.split()) == 3 and parse.is_date(updated.message.text.split()[1]) and \
            parse.is_date(updated.message.text.split()[2]):
        updated.message.reply_text("Считаем среднее на диапазоне между указанными датами")
        _, start, end = updated.message.text.split()
        res = stats.calculate_avg(updated.message.from_user.id, start, end)
    else:
        updated.message.reply_text("Введите просто /avg или /max с указанием двух дат (Y-m-d)")
        return POSTPROCESSING
    if res is None:
        updated.message.reply_text("Вы точно ввели даты в формате Y-m-d? А файл точно не удаляли?")
        return POSTPROCESSING
    updated.message.reply_text(f"Avg = {res}")
    return POSTPROCESSING


def find_median(updated: {types.Message}, _:Any)->int:
    """
    This function sends median to the user.

    :param updated: Message - updated wrapper of message
    """
    if len(updated.message.text.split()) == 1:
        updated.message.reply_text("Считаем медиану на всем диапазоне данных")
        res = stats.calculate_median(updated.message.from_user.id)
    elif len(updated.message.text.split()) == 3 and parse.is_date(updated.message.text.split()[1]) and \
            parse.is_date(updated.message.text.split()[2]):
        updated.message.reply_text("Считаем среднее на диапазоне между указанными датами")
        _, start, end = updated.message.text.split()
        res = stats.calculate_median(updated.message.from_user.id, start, end)
    else:
        updated.message.reply_text("Введите просто /avg или /avg с указанием двух дат (Y-m-d)")
        return POSTPROCESSING
    if res is None:
        updated.message.reply_text("Вы точно ввели даты в формате Y-m-d? А файл точно не удаляли?")
        return POSTPROCESSING
    updated.message.reply_text(f"Median = {res}")
    return POSTPROCESSING


def find_std(updated: {types.Message}, _:Any)->int:
    """
    This function sends standard deviation to the user.

    :param updated: Message - updated wrapper of message
    """
    if len(updated.message.text.split()) == 1:
        updated.message.reply_text("Считаем среднее на всем диапазоне данных")
        res = stats.calculate_avg(updated.message.from_user.id)
    elif len(updated.message.text.split()) == 3 and parse.is_date(updated.message.text.split()[1]) and \
            parse.is_date(updated.message.text.split()[2]):
        updated.message.reply_text("Считаем средне-квадратичное отклонение на диапазоне между указанными датами")
        _, start, end = updated.message.text.split()
        res = stats.calculate_avg(updated.message.from_user.id, start, end)
    else:
        updated.message.reply_text("Введите просто /std или /std с указанием двух дат (Y-m-d)")
        return POSTPROCESSING
    if res is None:
        updated.message.reply_text("Вы точно ввели даты в формате Y-m-d? А файл точно не удаляли?")
        return POSTPROCESSING
    updated.message.reply_text(f"Std = {res}")
    return POSTPROCESSING


def plot(updated: {types.Message}, _:Any)->int:
    """
    This function sends the user a plot of exchange dynamics.

    :param updated: Message - updated wrapper of message
    """
    if len(updated.message.text.split()) == 1:
        updated.message.reply_text("Строим график на всем диапазоне данных")
        res = stats.plot_dinamics(updated.message.from_user.id)
    elif len(updated.message.text.split()) == 3 and parse.is_date(updated.message.text.split()[1]) and \
            parse.is_date(updated.message.text.split()[2]):
        updated.message.reply_text("Строим график на диапазоне между указанными датами")
        _, start, end = updated.message.text.split()
        res = stats.plot_dinamics(updated.message.from_user.id, start, end)
    else:
        updated.message.reply_text("Введите просто /plot или /plot с указанием двух дат (Y-m-d)")
        return POSTPROCESSING
    if res is None:
        updated.message.reply_text("Вы точно ввели даты в формате Y-m-d? А файл точно не удаляли?")
        return POSTPROCESSING
    bot.send_photo(updated.message.from_user.id, photo=open(f"files/{updated.message.from_user.id}.png", "rb"))
    return POSTPROCESSING


if __name__ == "__main__":
    updater = Updater(API_TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(  # здесь строится логика разговора
        entry_points=[CommandHandler('start', send_welcome)],
        states={
            UPLOAD: [MessageHandler(Filters.document & (
                        Filters.document.mime_type("application/json") | Filters.document.mime_type("text/csv")),
                                    handle_docs)],
            POSTPROCESSING: [CommandHandler('min', find_min), CommandHandler('max', find_max),
                             CommandHandler('avg', find_avg),  CommandHandler('med', find_median),
                             CommandHandler('std', find_std),  CommandHandler('plot', plot)
                             ],
        },
        fallbacks=[CommandHandler('cancel', cancel), CommandHandler('delete', delete)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()
