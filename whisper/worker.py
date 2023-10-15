target_sample_rate = 16000
converted_file_name = "output_16kHz.wav"
wav_file_name = "out.wav"
output_file_name_without_extension = "output"

path_to_whisper = "./whisper.cpp/"
path_to_main = path_to_whisper + "main"
path_to_models = path_to_whisper + "models/"
large_model = path_to_models + "ggml-large.bin"


def get_ffmpeg_args_to_16khz(i_file_name, o_file_name):
    return f"ffmpeg -i {i_file_name} -ar 16000 {o_file_name}"


def get_ffmpeg_args_to_wav(i_file_name, o_file_name):
    return ["ffmpeg", "-i", i_file_name, "-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000", o_file_name]


def get_whisper_args(file_name):
    return [
        path_to_main,
        "-m",
        large_model,
        "-nt",
        "-otxt",
        "-l",
        "ru",
        "-pp",
        "-f",
        file_name,
        "-of",
        output_file_name_without_extension,
    ]
