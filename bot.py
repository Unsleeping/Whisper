import config
import utils
import random
import gdown
from telebot.apihelper import ApiTelegramException
from telebot import types
from utils import bot


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
                     utils.get_introducing(message.from_user.first_name, bot.get_me().first_name),
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
    chat_id = utils.get_chat_id(message)

    def worker():
        url = message.text
        if utils.is_gdrive_link(url):
            bot.send_message(chat_id, config.get_init_gdrive_message(), parse_mode='html')
            bot.send_sticker(chat_id, random.choice(config.loading_stickers))

            downloadable_url = utils.get_downloadable_url(url)
            file_name = gdown.download(downloadable_url, config.output_gdrive_file_name, quiet=False)

            bot.send_message(chat_id, config.get_download_complete_gdrive_message(), parse_mode='html')

            [output, file_to_remove] = utils.recognise_from_gdrive(file_name, utils.reply_to_user(chat_id))

            utils.send_result(chat_id, output, file_to_remove)

        else:
            bot.send_message(chat_id, config.get_error_message_no_gdrive_link(), parse_mode='html')

    start_worker(worker, lambda: utils.queued_fallback(chat_id))


@bot.message_handler(content_types=['audio'])
def add_audio(message):
    chat_id = utils.get_chat_id(message)

    def worker():
        try:
            audio = message.audio
            file_info = bot.get_file(audio.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            bot.send_message(chat_id, config.get_init_message(), parse_mode='html')
            bot.send_sticker(chat_id, random.choice(config.loading_stickers))

            [output, file_to_remove] = utils.recognise_from_file(audio, downloaded_file, utils.reply_to_user(chat_id))

            utils.send_result(chat_id, output, file_to_remove)

        except ApiTelegramException as e:
            error_message = config.get_error_message()
            if utils.is_file_size_limit_exceeded(e):
                error_message = config.get_error_message_file_size_exceeded()

            bot.send_message(chat_id, error_message, parse_mode='html')
            bot.send_sticker(chat_id, random.choice(config.error_stickers))

    start_worker(worker, lambda: utils.queued_fallback(chat_id))


if __name__ == '__main__':
    bot.polling(none_stop=True)
