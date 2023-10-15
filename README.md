🤖 **About WhisperBot**

WhisperBot simplifies audio to text on Telegram. Convert voice to text, enhance accessibility, and streamline workflows in seconds.

🔊 **Features:**

- Audio Conversion: Turn various audio formats into WAV files for optimal processing, using ffmpeg.
- Speech-to-Text: Use [whisper.cpp](https://github.com/ggerganov/whisper.cpp) library for accurate transcription.
- Telegram Integration: Seamless audio processing within your chats.
- Privacy Priority: Process audio files locally for security.

📢 **Why WhisperBot?**

- Accessibility: Convert lectures, interviews, and voice notes into text for easy sharing.
- Analysis: Extract insights from spoken content for research and content creation.
- Automation: Streamline tasks by automating time-consuming transcriptions.

🌟 Elevate your audio experience with WhisperBot. Convert audio to text effortlessly, enhance accessibility, and streamline your Telegram workflows!


# How to run 

If you don't run on mac with arch chips, you should remove `UNAME_M=arm64 UNAME_P=arm LLAMA_NO_METAL=1` before `make` command from all dockerfile


Then add .env-secrets with BOT_TOKEN=<your_telegram_bot_token>

and finally: 

    docker-compose up --build -d