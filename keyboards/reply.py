from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

main_keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="📝 Создать задачу"),
                KeyboardButton(text="📋 Мои задачи"),
            ],
            [
                KeyboardButton(text="📅 Задачи на сегодня"),
                KeyboardButton(text="🔮 Будущие задачи"),
            ],
            [
                KeyboardButton(text="⚙️ Настройки"),
            ],
        ]
    )


def cancel_keyboard():
    """Клавиатура с кнопкой отмены"""
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="❌ Отмена"))

    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Введите данные или нажмите 'Отмена'",
    )
