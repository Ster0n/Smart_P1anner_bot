from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Функция обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я Smart_P1anner_bot. Я помогу тебе вести список задач.")

# Создаём приложение с указанием токена и настройкой тайм-аутов
app = ApplicationBuilder().token("7884513282:AAFhHDsbr63H6VJBTj2tNI6GV7rdEztxi5I").build()

# Добавляем обработчик команды /start
app.add_handler(CommandHandler("start", start))

# Запускаем бота с опцией polling для получения сообщений
app.run_polling(timeout=30)  # Увеличиваем тайм-аут до 30 секунд

