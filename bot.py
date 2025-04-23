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
    [["Старт", "Создать задачу"], ["📅 Просмотр задач", "✅ Выполнить задачу"], ["🗑 Удалить задачу", "✏️ Редактировать задачу"]],
    resize_keyboard=True
)

keyboard_create_task = ReplyKeyboardMarkup(
    [["Отменить задачу"]],
    resize_keyboard=True
)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Выберите, что вам нужно:",
        reply_markup=keyboard_start
    )

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Старт":
        await update.message.reply_text(
            "Привет! Я Smart_P1anner_bot. Я помогу тебе вести список задач.",
            reply_markup=keyboard_start
        )

    elif text == "Создать задачу":
        context.user_data.clear()
        context.user_data["creating_task"] = True
        context.user_data["step"] = "name"
        await update.message.reply_text("Введите название задачи:", reply_markup=keyboard_create_task)

    elif text == "Отменить задачу":
        context.user_data.clear()
        await update.message.reply_text("Действие отменено.", reply_markup=keyboard_start)

    elif text == "📅 Просмотр задач":
        if tasks:
            task_list = "\n".join(
                f"{i + 1}. {'✅' if task['done'] else '🔲'} {task['name']} — {task['description']} (Дедлайн: {task['deadline']})"
                for i, task in enumerate(tasks)
            )
            await update.message.reply_text(f"📋 Список задач:\n{task_list}")
        else:
            await update.message.reply_text("Список задач пуст.")

    elif text == "✅ Выполнить задачу":
        if tasks:
            context.user_data.clear()
            context.user_data["marking_done"] = True
            task_list = "\n".join(
                f"{i + 1}. {'✅' if task['done'] else '🔲'} {task['name']}" for i, task in enumerate(tasks)
            )
            await update.message.reply_text(
                f"Введите номер задачи, которую хотите отметить как выполненную:\n{task_list}",
                reply_markup=keyboard_create_task
            )
        else:
            await update.message.reply_text("Список задач пуст.")

    elif text == "🗑 Удалить задачу":
        if tasks:
            context.user_data.clear()
            context.user_data["deleting_task"] = True
            task_list = "\n".join(
                f"{i + 1}. {'✅' if task['done'] else '🔲'} {task['name']}" for i, task in enumerate(tasks)
            )
            await update.message.reply_text(
                f"Введите номер задачи для удаления:\n{task_list}",
                reply_markup=keyboard_create_task
            )
        else:
            await update.message.reply_text("Список задач пуст.")

    elif text == "✏️ Редактировать задачу":
        if tasks:
            context.user_data.clear()
            context.user_data["editing_task"] = True
            task_list = "\n".join(
                f"{i + 1}. {'✅' if task['done'] else '🔲'} {task['name']} — {task['description']} (Дедлайн: {task['deadline']})"
                for i, task in enumerate(tasks)
            )
            await update.message.reply_text(
                f"Введите номер задачи для редактирования:\n{task_list}",
                reply_markup=keyboard_create_task
            )
        else:
            await update.message.reply_text("Список задач пуст.")

    elif context.user_data.get("creating_task"):
        step = context.user_data.get("step")

        if step == "name":
            context.user_data["task_name"] = text
            context.user_data["step"] = "description"
            await update.message.reply_text("Введите описание задачи:")

        elif step == "description":
            context.user_data["task_description"] = text
            context.user_data["step"] = "deadline"
            await update.message.reply_text("Введите дедлайн задачи (например, 25.04.2025):")

        elif step == "deadline":
            task = {
                "name": context.user_data["task_name"],
                "description": context.user_data["task_description"],
                "deadline": text,
                "done": False
            }
            tasks.append(task)
            context.user_data.clear()
            await update.message.reply_text(
                f"✅ Задача добавлена:\n*{task['name']}* — {task['description']} (Дедлайн: {task['deadline']})",
                reply_markup=keyboard_start
            )

    elif context.user_data.get("marking_done"):
        try:
            index = int(text) - 1
            if 0 <= index < len(tasks):
                tasks[index]["done"] = True
                task = tasks[index]
                await update.message.reply_text(
                    f"Задача '{task['name']}' отмечена как выполненная ✅",
                    reply_markup=keyboard_start
                )
            else:
                await update.message.reply_text("Неверный номер задачи.", reply_markup=keyboard_start)
        except ValueError:
            await update.message.reply_text("Введите корректный номер задачи.", reply_markup=keyboard_start)

        context.user_data.clear()

    elif context.user_data.get("deleting_task"):
        try:
            index = int(text) - 1
            if 0 <= index < len(tasks):
                removed_task = tasks.pop(index)
                await update.message.reply_text(
                    f"🗑 Задача '{removed_task['name']}' удалена.",
                    reply_markup=keyboard_start
                )
            else:
                await update.message.reply_text("Неверный номер задачи.", reply_markup=keyboard_start)
        except ValueError:
            await update.message.reply_text("Введите корректный номер задачи.", reply_markup=keyboard_start)

        context.user_data.clear()

    elif context.user_data.get("editing_task"):
        try:
            index = int(text) - 1
            if 0 <= index < len(tasks):
                context.user_data["edit_index"] = index
                context.user_data["step"] = "new_name"
                context.user_data["editing_task"] = False
                await update.message.reply_text("Введите новое название задачи:")
            else:
                await update.message.reply_text("Неверный номер задачи.", reply_markup=keyboard_start)
                context.user_data.clear()
        except ValueError:
            await update.message.reply_text("Введите корректный номер задачи.", reply_markup=keyboard_start)
            context.user_data.clear()

    elif context.user_data.get("step") == "new_name":
        context.user_data["new_name"] = text
        context.user_data["step"] = "new_description"
        await update.message.reply_text("Введите новое описание задачи:")

    elif context.user_data.get("step") == "new_description":
        context.user_data["new_description"] = text
        context.user_data["step"] = "new_deadline"
        await update.message.reply_text("Введите новый дедлайн задачи (например, 25.04.2025):")

    elif context.user_data.get("step") == "new_deadline":
        index = context.user_data["edit_index"]
        tasks[index]["name"] = context.user_data["new_name"]
        tasks[index]["description"] = context.user_data["new_description"]
        tasks[index]["deadline"] = text
        await update.message.reply_text(
            f"✏️ Задача обновлена:\n*{tasks[index]['name']}* — {tasks[index]['description']} (Дедлайн: {tasks[index]['deadline']})",
            reply_markup=keyboard_start
        )
        context.user_data.clear()

    else:
        await update.message.reply_text("Я не понимаю эту команду. Используйте кнопки.")

# Запуск бота
app = ApplicationBuilder().token(api_key).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
app.run_polling(timeout=30)
