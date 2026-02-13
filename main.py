import telebot
import subprocess
import os

BOT_TOKEN = "8034320169:AAHQf7DL52_ldmMqiM4Q7r2eWSRFK5-Tw9A"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@bot.message_handler(commands=["start"])
def start(m):
    bot.reply_to(
        m,
        "👋 <b>Welcome!</b>\n\n📥 Just send any video link.\nI will download & send it back."
    )

@bot.message_handler(func=lambda m: True)
def downloader(m):
    url = m.text.strip()

    msg = bot.reply_to(m, "⏳ Downloading...")

    try:
        cmd = [
            "yt-dlp",
            "-f", "mp4",
            "-o", f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
            url
        ]

        subprocess.run(cmd, check=True)

        files = os.listdir(DOWNLOAD_DIR)
        if not files:
            bot.edit_message_text("❌ Download failed.", m.chat.id, msg.message_id)
            return

        filepath = os.path.join(DOWNLOAD_DIR, files[0])

        with open(filepath, "rb") as f:
            bot.send_video(m.chat.id, f)

        os.remove(filepath)
        bot.delete_message(m.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ Error:\n<code>{e}</code>", m.chat.id, msg.message_id)

print("Bot running...")
bot.infinity_polling()
