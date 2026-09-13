import os
from dotenv import load_dotenv
from telegram import Update 
from telegram.ext import Application, MessageHandler, filters, ContextTypes 
from google import genai
from google.genai import types 


load_dotenv()
telegram_token = os.getenv("telegram_bot_token")
gemini_api_key = os.getenv("gemini_api_key")
client = genai.Client(api_key=gemini_api_key)

async def balas_pesan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pesan_user = update.message.text
    try :
        response = client.models.generate_content(
            model = 'gemini-3.5-flash',
            contents = pesan_user

         )
        return await update.message.reply_text(response.text)
    except Exception as e :
        print("response gagal :", e)
        await update.message.reply_text("maaf, lagi ada gangguan. coba lagi beberapa saat ya")
    return None


app = Application.builder().token(telegram_token).build()
app.add_handler(MessageHandler(filters.TEXT, balas_pesan))
app.run_polling()