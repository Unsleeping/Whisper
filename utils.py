import config
import os
import re
import telebot
import random
import wave
from config import output_name

bot = telebot.TeleBot(config.token)
queued = False


def get_sample_rate(wav_file):
    with wave.open(wav_file, 'rb') as wf:
        return wf.getframerate()


def reply_to_user(chat_id):
    return lambda log: bot.send_message(chat_id, log)


def get_result():
    if os.path.exists(output_name):
        text = open(output_name)
        return text

    return None


def send_result(chat_id, log):
    result = get_result()
    if result:
        log('Sending recognised text', is_user=True)
        bot.send_document(chat_id, result)
        remove(config.output_name, f'remove recognised text {config.output_name}')


def queued_fallback(chat_id):
    bot.send_message(chat_id, config.get_queued_message())
    bot.send_sticker(chat_id, random.choice(config.queued_stickers))


def get_chat_id(message):
    return message.chat.id


def is_gdrive_link(url):
    return "https://drive.google.com/" in url


def is_file_size_limit_exceeded(error):
    return "file is too big" in str(error)


def get_downloadable_url(url):
    return re.sub(r"https://drive\.google\.com/file/d/(.*?)/.*?\?usp=sharing",
                  r"https://drive.google.com/uc?id=\1", url)


def get_introducing(user_name, bot_name):
    return f"Hello {user_name}! I am - <b>{bot_name}</b>."


def console_log(message):
    print(f'>> {message}')


def get_logger(reply):
    def log(message, is_console=True, is_user=False):
        if is_console:
            console_log(message)
        if is_user:
            reply(message)

    return log


def remove(file_name, reason=''):
    if os.path.exists(file_name):
        if reason != '':
            console_log(reason)
        os.remove(file_name)
