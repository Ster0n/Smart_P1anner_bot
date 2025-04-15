from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, ContextTypes, filters
)
from dotenv import load_dotenv
import os

# Загружаем переменные из .env
load_dotenv()
api_key = os.getenv("TELEGRAM_API_KEY")

# Список задач (пока в памяти)
tasks = []

# Клавиатура с кнопками
keyboard_start = ReplyKeyboardMarkup(
    [["Старт", "Создать задачу"], ["📅 Просмотр задач"]],
    resize_keyboard=True
)

keyboard_create_task = ReplyKeyboardMarkup(
    [["Отменить задачу"]],
    resize_keyboard=True
)

# Команда /start — приветствие и отображение кнопок
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Выберите, что вам нужно:",
        reply_markup=keyboard_start
    )

# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Старт":
        await update.message.reply_text(
            "Привет! Я Smart_P1anner_bot. Я помогу тебе вести список задач.",
            reply_markup=keyboard_start
        )

    elif text == "Создать задачу":
        await update.message.reply_text("Введите текст задачи:")
        context.user_data["creating_task"] = True
        await update.message.reply_text("Для отмены нажмите 'Отменить задачу'", reply_markup=keyboard_create_task)

    elif text == "Отменить задачу":
        context.user_data["creating_task"] = False
        await update.message.reply_text("Создание задачи отменено.", reply_markup=keyboard_start)

    elif text == "📅 Просмотр задач":
        if tasks:
            task_list = "\n".join(f"{i + 1}. {task}" for i, task in enumerate(tasks))
            await update.message.reply_text(f"📋 Список задач:\n{task_list}")
        else:
            await update.message.reply_text("Список задач пуст.")

    elif context.user_data.get("creating_task"):
        tasks.append(text)
        await update.message.reply_text(f"Задача добавлена: {text}", reply_markup=keyboard_start)
        context.user_data["creating_task"] = False

    else:
        await update.message.reply_text("Я не понимаю эту команду. Используйте кнопки.")

# Настройка и запуск бота
app = ApplicationBuilder().token(api_key).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
app.run_polling(timeout=30)
