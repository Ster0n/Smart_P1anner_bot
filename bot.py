from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv
import os

# Загружаем переменные из .env
load_dotenv()
api_key = os.getenv("TELEGRAM_API_KEY")

# Список задач (в памяти)
tasks = []

# Клавиатуры
keyboard_start = ReplyKeyboardMarkup(
    [["Старт", "Создать задачу"], ["📅 Просмотр задач"]],
    resize_keyboard=True
)

keyboard_create_task = ReplyKeyboardMarkup(
    [["Отменить задачу"]],
    resize_keyboard=True
)

# Команда /start — приветствие и кнопки
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Выберите, что вам нужно:",
        reply_markup=keyboard_start
    )

# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Приветствие
    if text == "Старт":
        await update.message.reply_text(
            "Привет! Я Smart_P1anner_bot. Я помогу тебе вести список задач.",
            reply_markup=keyboard_start
        )

    # Начало создания задачи
    elif text == "Создать задачу":
        context.user_data.clear()
        context.user_data["creating_task"] = True
        context.user_data["step"] = "name"
        await update.message.reply_text("Введите название задачи:", reply_markup=keyboard_create_task)

    # Отмена создания задачи
    elif text == "Отменить задачу":
        context.user_data.clear()
        await update.message.reply_text("Создание задачи отменено.", reply_markup=keyboard_start)

    # Просмотр списка задач
    elif text == "📅 Просмотр задач":
        if tasks:
            task_list = "\n".join(
                f"{i + 1}. {task['name']} — {task['description']}" for i, task in enumerate(tasks)
            )
            await update.message.reply_text(f"📋 Список задач:\n{task_list}")
        else:
            await update.message.reply_text("Список задач пуст.")

    # Пошаговое добавление задачи
    elif context.user_data.get("creating_task"):
        step = context.user_data.get("step")

        if step == "name":
            context.user_data["task_name"] = text
            context.user_data["step"] = "description"
            await update.message.reply_text("Введите описание задачи:")

        elif step == "description":
            task_name = context.user_data.get("task_name")
            task_description = text
            tasks.append({
                "name": task_name,
                "description": task_description,
                "done": False
            })
            context.user_data.clear()
            await update.message.reply_text(
                f"✅ Задача добавлена:\n*{task_name}* — {task_description}",
                reply_markup=keyboard_start
            )

    # Неизвестная команда
    else:
        await update.message.reply_text("Я не понимаю эту команду. Используйте кнопки.")

# Запуск бота
app = ApplicationBuilder().token(api_key).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
app.run_polling(timeout=30)