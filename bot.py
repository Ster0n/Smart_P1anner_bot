from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv
import os

# Загружаем переменные из .env
load_dotenv()
api_key = os.getenv("TELEGRAM_API_KEY")

# Клавиатура с кнопкой "Старт"
keyboard = ReplyKeyboardMarkup(
    [["Старт"]],
    resize_keyboard=True
)

# Команда /start — приветствие и отображение кнопки
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Выберите, что вам нужно:",
        reply_markup=keyboard
    )

# Обработка нажатия на кнопку "Старт"
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Старт":
        await update.message.reply_text("Привет! Я Smart_P1anner_bot. Я помогу тебе вести список задач.")

# Настройка и запуск бота
app = ApplicationBuilder().token(api_key).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

# Запускаем бота с опцией polling для получения сообщений
app.run_polling(timeout=30)  # Увеличиваем тайм-аут до 30 секунд

