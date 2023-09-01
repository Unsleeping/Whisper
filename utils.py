import config
import subprocess
import os
import mimetypes
import re
import telebot
import random

bot = telebot.TeleBot(config.token)


def reply_to_user(chat_id):
    return lambda log: bot.send_message(chat_id, log)


def send_result(chat_id, output, file_to_remove):
    bot.send_document(chat_id, output)
    remove(file_to_remove, f'>> remove recognised text {file_to_remove}')


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


def set_logger(reply):
    def log(message, is_console=True, is_user=False):
        if is_console:
            print(f'>> {message}')
        if is_user:
            reply(message)

    return log


def run_speech_recognition(file_name, reply):
    log = set_logger(reply)
    log('I started speech recognition', is_user=True)
    subprocess.call(config.get_whisper_args(file_name))
    log('I finished speech recognition', is_user=True)
    remove(file_name, '>> remove source audio')

    output_name = file_name + txt_extension_string
    if os.path.exists(output_name):
        text = open(output_name)
        log('Sending recognised text', is_user=True)
        return [text, output_name]


def remove(file_name, reason=''):
    if os.path.exists(file_name):
        if reason != '':
            print(reason)
        os.remove(file_name)


def recognise(mime_type, file_name, reply):
    log = set_logger(reply)
    is_wav = mime_type == 'audio/x-wav'
    if is_wav:
        log('uploaded file is WAV')
        return run_speech_recognition(file_name, reply)
    else:
        log('Provided file needs to be converted first into WAV before recognition, I\'m working on it now',
            is_user=True)
        subprocess.call(config.get_ffmpeg_args(file_name, config.output_file_name))
        log('Conversion is finished', is_user=True)
        remove(file_name, '>> remove original audio')
        return run_speech_recognition(config.output_file_name, reply)


def recognise_from_gdrive(name, reply):
    return recognise(mimetypes.guess_type(name)[0], name, reply)


def recognise_from_file(audio, file, reply):
    file_name = audio.file_name
    with open(file_name, 'wb') as new_file:
        new_file.write(file)

    return recognise(audio.mime_type, new_file.name, reply)


queued = False
txt_extension_string = '.txt'
