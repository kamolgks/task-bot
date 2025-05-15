# 📋 TASK-BOT

> Telegram-бот для управления личными задачами — просто, эффективно и вовремя.

![Last Commit](https://img.shields.io/github/last-commit/kamolgks/task-bot?style=flat-square)
![Python](https://img.shields.io/badge/python-3.10+-blue?style=flat-square)
![License](https://img.shields.io/github/license/kamolgks/task-bot?style=flat-square)
![aiogram](https://img.shields.io/badge/aiogram-3.x-blue?style=flat-square)
![Redis](https://img.shields.io/badge/Redis-enabled-critical?style=flat-square)

## 🛠 Используемые технологии:

![Python](https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Aiogram](https://img.shields.io/badge/-Aiogram-2C2D72?style=for-the-badge)
![SQLite](https://img.shields.io/badge/-SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Redis](https://img.shields.io/badge/-Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![FSM](https://img.shields.io/badge/-FSM-handling-9cf?style=for-the-badge)

---

## 📚 Содержание

- [Обзор](#обзор)
- [Функциональность](#функциональность)
- [Запуск проекта](#запуск-проекта)
  - [Зависимости](#зависимости)
  - [Установка](#установка)
  - [Настройка](#настройка)
  - [Запуск бота](#запуск-бота)
- [Структура проекта](#структура-проекта)
- [Лицензия](#лицензия)
- [Автор](#автор)

---

## 📖 Обзор

**Task-Bot** — это телеграм-бот, помогающий управлять задачами. Он позволяет создавать, просматривать и удалять задачи с учетом вашего часового пояса. Имеет удобный интерфейс и напоминания.

---

## ✨ Функциональность

- Добавление задач с описанием, датой и временем
- Просмотр всех задач, задач на сегодня и предстоящих
- Удаление задач
- Установка часового пояса пользователя
- Напоминания по времени
- Удобные клавиатуры
- Хранение состояний через Redis и FSM

---

## ⚙️ Запуск проекта

### ✅ Зависимости

- Python 3.10+
- Redis (для хранения состояний)
- Telegram Bot Token от [BotFather](https://t.me/BotFather)

### 📥 Установка

```bash
git clone https://github.com/kamolgks/task-bot.git
cd task-bot
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### ⚙️ Настройка

Создайте файл `.env` на основе шаблона:

```bash
cp .env.example .env
```

И укажите свои значения:

```env
BOT_TOKEN=ваш_токен_бота
REDIS_HOST=localhost
REDIS_PORT=6379
```

### 🚀 Запуск бота

```bash
python main.py
```

---

## 🗂 Структура проекта

```
task-bot/
├── database/           # Работа с базой SQLite
├── fsm/                # Машины состояний пользователя
├── handlers/           # Обработчики сообщений
├── keyboards/          # Интерфейс (reply/inline клавиатуры)
├── main.py             # Точка входа
├── config.py           # Конфигурация
├── requirements.txt    # Зависимости проекта
├── .env.example        # Шаблон переменных окружения
```

---

## 📄 Лицензия

Проект распространяется под лицензией MIT. Подробнее в файле [LICENSE](LICENSE).

---

## 🤝 Автор

Разработчик: [Kamoliddin Tukhtaboev](https://github.com/kamolgks)

Если есть идеи, предложения или ошибки — создавай [issue](https://github.com/kamolgks/task-bot/issues) или pull request.

---
