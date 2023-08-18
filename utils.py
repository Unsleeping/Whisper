import config
import subprocess
import os


def get_chat_id(message):
    return message.chat.id


def get_introducing(user_name, bot_name):
    return "Hello {0}! I am - <b>{1}</b>.".format(user_name, bot_name)


def run_speech_recognition(file_name):
    print('>> start speech recognition', file_name)
    subprocess.call(config.get_whisper_args(file_name))
    print('>> finish speech recognition', file_name)
    remove(file_name, '>> remove source audio')

    output_name = file_name + txt_extension_string
    if os.path.exists(output_name):
        text = open(output_name)
        print('>> sending recognised text', output_name)
        return [text, output_name]


def remove(file_name, reason=''):
    if os.path.exists(file_name):
        if reason != '':
            print(reason)
        os.remove(file_name)


def start_recognition(audio, downloaded_file):
    file_name = audio.file_name
    is_wav = audio.mime_type == 'audio/x-wav'
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    if is_wav:
        print('>> uploaded file is WAV')
        return run_speech_recognition(new_file.name)
    else:
        print('>> uploaded file isn\'t WAV')
        print('>> converting {0.name} into WAV'.format(new_file))
        subprocess.call(config.get_ffmpeg_args(new_file.name, config.output_file_name))
        print('>> finish converting {0.name} into WAV'.format(new_file))
        remove(new_file.name, '>> remove original audio')
        return run_speech_recognition(config.output_file_name)


queued = False
txt_extension_string = '.txt'

