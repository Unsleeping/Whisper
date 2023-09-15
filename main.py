import mimetypes
import subprocess
from utils import remove, get_sample_rate
from worker import *


def convert_to_16khz(input_file, output_file):
    subprocess.run(get_ffmpeg_args_to_16khz(input_file, output_file), shell=True)


def check_rate(file_name, log):
    current_sample_rate = get_sample_rate(file_name)
    if current_sample_rate != target_sample_rate:
        log(f"Converting WAV file from {current_sample_rate}Hz to {target_sample_rate}Hz...", is_user=True)
        convert_to_16khz(file_name, converted_file_name)
        remove(file_name, 'remove original audio')
        return converted_file_name
    else:
        log(f"WAV file is already at {target_sample_rate}Hz.")
        return file_name


def convert_to_wav(file_name):
    subprocess.call(get_ffmpeg_args_to_wav(file_name, wav_file_name))
    remove(file_name, 'remove original audio')
    return wav_file_name


def run_speech_recognition(file_name, log):
    log('I started speech recognition', is_user=True)
    subprocess.call(get_whisper_args(file_name))
    log('I finished speech recognition', is_user=True)
    remove(file_name, 'remove source audio')


def recognise(mime_type, file_name, log):
    is_wav = mime_type == 'audio/x-wav'
    if is_wav:
        log('Uploaded file is WAV')
        file_to_proceed = check_rate(file_name, log)
    else:
        log('Provided file needs to be converted first into WAV before recognition, I\'m working on it now',
            is_user=True)
        file_to_proceed = convert_to_wav(file_name)
        log('Conversion is finished', is_user=True)

    return run_speech_recognition(file_to_proceed, log)


def recognise_from_file(audio, file, log):
    file_name = audio.file_name
    with open(file_name, 'wb') as new_file:
        new_file.write(file)
    return recognise(audio.mime_type, new_file.name, log)


def recognise_from_gdrive(name, log):
    return recognise(mimetypes.guess_type(name)[0], name, log)
