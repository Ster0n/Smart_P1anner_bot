from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я Smart_P1anner_bot. Я помогу тебе вести список задач.")

app = ApplicationBuilder().token("7884513282:AAFhHDsbr63H6VJBTj2tNI6GV7rdEztxi5I").build()
app.add_handler(CommandHandler("start", start))

app.run_polling()
