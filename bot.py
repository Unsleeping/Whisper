import telebot
import config
import utils
import random

from telebot import types

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start', 'Start'])
def start_message(message):
    keyboard2 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_language = types.KeyboardButton(text="/recognise")
    keyboard2.add(button_language)
    bot.send_message(message.chat.id,
                     utils.get_introducing(message.from_user.first_name, bot.get_me().first_name),
                     parse_mode='html',
                     reply_markup=keyboard2)
    bot.send_message(message.chat.id,
                     config.get_started_message())


@bot.message_handler(content_types=['sticker'])
def send_sticker(message):
    print(message.sticker.file_id)


@bot.message_handler(content_types=['audio'])
def addfile(message):
    chat_id = utils.get_chat_id(message)
    if utils.queued:
        bot.send_message(chat_id, config.get_queued_message())
        bot.send_sticker(chat_id, random.choice(config.queued_stickers))
        return None

    utils.queued = True
    bot.send_message(chat_id, config.get_init_message(), parse_mode='html')
    bot.send_sticker(chat_id, random.choice(config.loading_stickers))

    audio = message.audio
    file_info = bot.get_file(audio.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    [output, file_to_remove] = utils.start_recognition(audio, downloaded_file)

    bot.send_document(chat_id, output)
    utils.queued = False
    utils.remove(file_to_remove, '>> remove recognised text {0}'.format(file_to_remove))


if __name__ == '__main__':
    bot.polling(none_stop=True)