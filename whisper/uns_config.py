output_file_name_without_extension = "output"
txt_extension_string = ".txt"
output_name = output_file_name_without_extension + txt_extension_string

output_gdrive_file_name = "downloaded_file.m4a"

queued_stickers = ["CAACAgIAAxkBAAO-ZN_xxk80Rn7whXv3Vd52uR2woccAAsURAAKwmrFIXVGdvpClV9owBA"]
loading_stickers = [
    "CAACAgIAAxkBAANPZN-0gFHR-yuTDfabyL_thki1AAHpAAI5FgACmYxQSPiB6BR-_jYIMAQ",
    "CAACAgQAAxkBAANSZN-08l1M8wUF979kC53-xA9LVDgAAv4MAAIJ-8BS5S76dY9_OHgwBA",
    "CAACAgQAAxkBAANVZN-1ArdxnBVOTsuSEOcKmt9KqkwAAjsBAAKoISEGPOnkASRxsm0wBA",
    "CAACAgIAAxkBAANhZN-19dqJNsV745B1bkjBpeBJrFkAAo8VAALofwhIpNvkhqflmYYwBA",
    "CAACAgIAAxkBAANkZN-2J5t9usK3vNXFK6q8ZxgP3ccAAnMAA6tXxAsTtGy0UBg9kjAE",
    "CAACAgIAAxkBAANqZN-2YuMdCj-3nDi-ZbZs9F_3voAAApYRAAL-bYBJnV_SjR84kaUwBA",
    "CAACAgIAAxkBAANtZN-2frB5VlUK_GoDdpqBRTx6RIUAAl0AA4jMkRcH1bOVO5k1MjAE",
    "CAACAgIAAxkBAANwZN-2l-JUT2b5LdGoVKy4lPlnPTIAAlofAAI7dqhIUsC8jvRkLxEwBA",
    "CAACAgIAAxkBAANzZN-2qkHvAcU1vUVvhcxsoUwgXcIAAiYAA4jMkRdiooUyHk3TsTAE",
    "CAACAgIAAxkBAAN2ZN-3DWwxk68kjnUjSBK9UCkF-W8AAmQAA4jMkReBRg-EKwMmzjAE",
    "CAACAgIAAxkBAAN5ZN-3IHXkK9vN2aVckG9-7uvQt-0AAmgAA4jMkRfopqaqtILakDAE",
    "CAACAgIAAxkBAAN8ZN-3trFFAj7bclMgTyTp2qtAtJUAAq8lAAKbonBLuDnFfbteCGYwBA",
    "CAACAgIAAxkBAAN_ZN-3_RJ0SH686nwxbVZLQ2reGgAD0xIAAo6xaUkfw1YOxOnk2TAE",
]
error_stickers = [
    "CAACAgIAAxkBAAIBJ2TwpmzmN3hLT7bLpIemKV7hfaCNAAJHAwACbbBCA1JVK_k1xYCCMAQ",
    "CAACAgIAAxkBAAIBKGTwponwkocM6fqsHuuRqioCrbR0AAJbEwACuyEwSTPnlvEy-FrUMAQ",
    "CAACAgIAAxkBAAIBKWTwppkpq384gpwbBBRZIe35aCu7AAIIAQACVp29CgEbgpjRakthMAQ",
    "CAACAgIAAxkBAAIBKmTwpqntnSxA-kDLV_sfmbayx7m0AAIxAAOIzJEXsnampME3WgowBA",
    "CAACAgIAAxkBAAIBK2TwpsvKUA_wBE5CXbGIobhK8RF7AAJAAAOIzJEXBnAZIsVxxJ0wBA",
    "CAACAgIAAxkBAAIBLGTwpxhpKImds2EY7xPbG0w1c43vAAIrFAACt5nIS_UUz5bBuI9VMAQ",
]


def get_queued_message():
    return "Wait until the current file finishes processing before sending more commands"


def get_started_message():
    return (
        "I'm here to assist you in converting audio files into text using advanced speech recognition "
        + "technology.\n\n"
        + "Transform spoken words into written text for easy reference, analysis, "
        + "and accessibility. Whether it's an interview, a lecture, or any audio content, I've got you "
        + "covered.\n\n"
        + "To start recognition send the audio sample or provide a link from Google Drive on that file."
    )


def get_init_gdrive_message():
    return (
        "🔊 <b>Audio Conversion Initiated</b> \n\n"
        "Awesome! You've just taken the first step towards transforming your audio into text. 🎉\n\n"
        "🔗 <b>Link Received:</b> "
        "We've got your link,"
        " and WhisperBot is ready to download file to convert that audio into text.\n\n"
    )


def get_download_complete_gdrive_message():
    return (
        "🔄 <b>Processing:</b> "
        "Our WhisperBot is now hard at work,"
        " using advanced technology to transcribe the spoken content.\n\n"
        "⏳ <b>Please Wait:</b> "
        "The conversion process may take a moment, especially for longer recordings."
        "Your patience is much appreciated.\n\n"
        "📝 <b>Text Result:</b> "
        "Once the conversion is complete,"
        " you'll receive "
        "the text transcript right here in this chat."
    )


def get_error_message_no_gdrive_link():
    return "🛑 Seems that it's not a google drive link you have posted here"


def get_init_message():
    return (
        "🔊 <b>Audio Conversion Initiated</b> \n\n"
        "Awesome! You've just taken the first step towards transforming your audio into text. 🎉\n\n"
        "🎧 <b>Audio Received:</b> "
        "We've got your audio file,"
        " and WhisperBot is ready to convert it into text.\n\n"
        "🔄 <b>Processing:</b> "
        "Our WhisperBot is now hard at work,"
        " using advanced technology to transcribe the spoken content."
        "⏳ <b>Please Wait:</b> "
        "The conversion process may take a moment, especially for longer recordings."
        "Your patience is much appreciated.\n\n"
        "📝 <b>Text Result:</b> "
        "Once the conversion is complete,"
        " you'll receive "
        "the text transcript right here in this chat."
    )


def get_error_message():
    return (
        "👷🏽 Something went wrong, try again later"
        " or create an issue on <a>https://github.com/Unsleeping/Whisper/issues</a> "
    )


def get_error_message_file_size_exceeded():
    return (
        "🔧 <b>File size is more than 20 Mb</b> \n\n"
        "To proceed such files you need: \n\n"
        "1) to upload them into <a>https://drive.google.com/</a> \n\n"
        "2) send the link here, in the chat \n\n"
        "3) do not forget to open access to your file (on a share screen) \n\n"
    )
