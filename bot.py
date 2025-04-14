from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os

# Загружаем переменные из файла .env
load_dotenv()

# Получаем API-ключ из переменной окружения
api_key = os.getenv("TELEGRAM_API_KEY")

# Функция обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я Smart_P1anner_bot. Я помогу тебе вести список задач.")

# Создаём приложение с использованием API-ключа из .env
app = ApplicationBuilder().token(api_key).build()

# Добавляем обработчик команды /start
app.add_handler(CommandHandler("start", start))

# Запускаем бота с опцией polling для получения сообщений
app.run_polling(timeout=30)  # Увеличиваем тайм-аут до 30 секунд
