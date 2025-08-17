import os
import requests
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")
API_URL = "https://drlabapis.onrender.com/api/ccgenerator"

def parse_input(input_text):
    input_text = input_text.strip()
    count = 10

    parts_space = input_text.split()
    if len(parts_space) > 1 and parts_space[-1].isdigit():
        count = int(parts_space[-1])
        input_text = " ".join(parts_space[:-1])

    bin_input = input_text

    return bin_input, count

async def ccgen_advanced(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input_text = update.message.text.strip()
    bin_param, count = parse_input(input_text)

    params = {"bin": bin_param, "count": count}

    try:
        r = requests.get(API_URL, params=params)
        if r.status_code == 200:
            raw_ccs = r.text.strip().split('\n')

            message_lines = ["🃏 CREDIT CARD GENERATOR 🃏\n"]
            message_lines.append("```")
            message_lines.extend(raw_ccs)
            message_lines.append("```")

            message = "\n".join(message_lines)
            await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
        else:
            await update.message.reply_text(
                f"❌ Gagal mendapatkan data dari API. Status code: {r.status_code}"
            )
    except Exception as e:
        await update.message.reply_text(f"⚠️ Terjadi kesalahan: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN_BOT).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ccgen_advanced))
    print("BOT RUNNING...")
    app.run_polling()
