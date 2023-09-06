import config
import utils
import random
import gdown
from telebot.apihelper import ApiTelegramException
from telebot import types
from utils import (bot, send_result, get_introducing, get_chat_id, get_logger, reply_to_user, is_gdrive_link,
                   queued_fallback, is_file_size_limit_exceeded, get_downloadable_url)
from main import recognise_from_file, recognise_from_gdrive


def start_worker(callback, fallback):
    if utils.queued:
        fallback()

    utils.queued = True
    callback()
    utils.queued = False


@bot.message_handler(commands=['start', 'Start'])
def start_message(message):
    keyboard1 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard2 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_start = types.KeyboardButton(text="/start")
    button_recognise = types.KeyboardButton(text="/recognise")
    keyboard1.add(button_start)
    keyboard2.add(button_recognise)
    bot.send_message(message.chat.id,
                     get_introducing(message.from_user.first_name, bot.get_me().first_name),
                     parse_mode='html',
                     reply_markup=keyboard2)
    bot.send_message(message.chat.id,
                     config.get_started_message())


@bot.message_handler(content_types=['sticker'])
def send_sticker(message):
    print(message.sticker.file_id)


@bot.message_handler(content_types=['text'])
def get_link(message):
    print(message.text)
    chat_id = get_chat_id(message)
    log = get_logger(reply_to_user(chat_id))

    def worker():
        url = message.text
        if is_gdrive_link(url):
            bot.send_message(chat_id, config.get_init_gdrive_message(), parse_mode='html')
            bot.send_sticker(chat_id, random.choice(config.loading_stickers))

            downloadable_url = get_downloadable_url(url)
            file_name = gdown.download(downloadable_url, config.output_gdrive_file_name, quiet=False)

            bot.send_message(chat_id, config.get_download_complete_gdrive_message(), parse_mode='html')

            recognise_from_gdrive(file_name, log)
            send_result(chat_id, log)

        else:
            bot.send_message(chat_id, config.get_error_message_no_gdrive_link(), parse_mode='html')

    start_worker(worker, lambda: queued_fallback(chat_id))


@bot.message_handler(content_types=['audio'])
def add_audio(message):
    chat_id = get_chat_id(message)
    log = get_logger(reply_to_user(chat_id))

    def worker():
        try:
            audio = message.audio
            file_info = bot.get_file(audio.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            bot.send_message(chat_id, config.get_init_message(), parse_mode='html')
            bot.send_sticker(chat_id, random.choice(config.loading_stickers))

            recognise_from_file(audio, downloaded_file, log)
            send_result(chat_id, log)

        except ApiTelegramException as e:
            error_message = config.get_error_message()
            if is_file_size_limit_exceeded(e):
                error_message = config.get_error_message_file_size_exceeded()

            bot.send_message(chat_id, error_message, parse_mode='html')
            bot.send_sticker(chat_id, random.choice(config.error_stickers))

    start_worker(worker, lambda: queued_fallback(chat_id))


if __name__ == '__main__':
    bot.polling(none_stop=True)
