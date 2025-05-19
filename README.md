
# 📘 Smart_P1anner_bot

**Smart_P1anner_bot** — это Telegram-бот на Python, помогающий вести список задач. Поддерживает добавление, редактирование, выполнение и удаление задач с удобным управлением через кнопки.

## 🔧 Функции

- 🆕 **Создание задач** — бот поэтапно запрашивает название, описание и дедлайн.
- 📅 **Просмотр задач** — вывод всех задач с обозначением выполненных.
- ✅ **Отметка задач как выполненных** — возможность пометить задачу завершённой.
- 🗑 **Удаление задач** — выбор задачи по номеру и удаление.
- ✏️ **Редактирование задач** — изменение названия, описания и дедлайна.
- 🚫 **Отмена действия** — отмена создания/редактирования/удаления задачи в любой момент.
- 🧠 **Хранение задач в памяти** — данные сохраняются в оперативной памяти (временное хранение).

## 🚀 Запуск

1. Установите зависимости:

```bash
pip install python-telegram-bot==20.0b0 python-dotenv
```

2. Создайте `.env` файл в корне проекта и добавьте ваш API-ключ:

```
TELEGRAM_API_KEY=ваш_ключ_бота
```

3. Запустите бота:

```bash
python bot.py
```

## 🖼 Пример интерфейса

После команды `/start` или нажатия "Старт", пользователю будет доступна клавиатура:

```
[Старт]  [Создать задачу]
[📅 Просмотр задач] [✅ Выполнить задачу]
[🗑 Удалить задачу] [✏️ Редактировать задачу]
```

## 📝 Пример задачи

```text
🔲 Учёба — Подготовить курсовую работу (Дедлайн: 25.05.2025)
✅ Фитнес — Тренировка в зале (Дедлайн: 19.05.2025)
```

## 📌 Технические детали

- Язык: Python 3
- Фреймворк: `python-telegram-bot`
- Хранение данных: оперативная память (список `tasks`)
- Архитектура: один файл `bot.py`, использует `ContextTypes` для хранения данных пользователя

## 📍 TODO

- [ ] Подключение базы данных или JSON-файла для хранения задач
- [ ] Уведомления о приближении дедлайна
- [ ] Авторизация по ID пользователя
- [ ] Мультипользовательский режим
- [ ] Инлайн-кнопки

## 👨‍💻 Автор

**Береговой Степан Сергеевич**  
Telegram: [@Steron404](https://t.me/Steron404)  
Email: beregovoy2002123@gmail.com


---

## English Description

### Smart_P1anner_bot

Smart_P1anner_bot is a simple Telegram-based task planner developed using `python-telegram-bot`. It allows users to manage their task list with an intuitive chat interface.

### Features

- 👋 Start the bot and receive a greeting
- ✅ Create new tasks with name, description, and deadline
- 📅 View the full list of tasks with status indicators
- 🟩 Mark tasks as completed
- 🗑 Delete tasks from the list
- ✏️ Edit task details (name, description, deadline)
- ❌ Cancel task creation at any time

### Requirements

- Python 3.10+
- python-telegram-bot
- python-dotenv

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Smart_P1anner_bot.git
   cd Smart_P1anner_bot/v0.1
   ```

2. Create a `.env` file in the project root and add your bot token:
   ```env
   TELEGRAM_API_KEY=your_telegram_bot_token
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the bot:
   ```bash
   python bot.py
   ```

Enjoy planning your tasks with Smart_P1anner_bot! 🎯
