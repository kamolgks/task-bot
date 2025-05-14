from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def tasks_keyboard(tasks, action="view"):
    """
    Создает инлайн-клавиатуру для списка задач
    """
    builder = InlineKeyboardBuilder()

    for task in tasks:
        button_text = f"{task['name']} ({task['time']})"

        if action == "delete":
            callback_data = f"confirm_delete:{task['id']}" # delete_task:{task['id']}
        else:
            callback_data = f"view_task:{task['id']}"

        builder.add(InlineKeyboardButton(text=button_text, callback_data=callback_data))

    # builder.add(InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_tasks"))
    # builder.adjust(1)
    return builder.as_markup()


def confirm_delete(task_id):
    """
    Создает клавиатуру для подтверждения удаления задачи
    """
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="✅ Да, удалить", callback_data=f"delete_task:{task_id}"),
        InlineKeyboardButton(text="❌ Нет, отмена", callback_data="cancel_action"),
    )

    return builder.as_markup()


def task_actions(task_id):
    """
    Создает клавиатуру действий для конкретной задачи
    """
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"delete_task:{task_id}"),
        InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_tasks"),
    )

    return builder.as_markup()


def settings_keyboard():
    """
    Создает клавиатуру настроек
    """
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🌐 Изменить часовой пояс", callback_data="change_timezone"))
    return builder.as_markup()

def timezone_keyboard():
    """
    Создает клавиатуру выбора часового пояса
    """
    builder = InlineKeyboardBuilder()
    timezones = [
        ("+2", "UTC+2"), ("+3", "UTC+3"), ("+4", "UTC+4"),
        ("+5", "UTC+5"), ("+6", "UTC+6"), ("+7", "UTC+7"),
        ("+8", "UTC+8"), ("+9", "UTC+9"), ("+10", "UTC+10"),
        ("+11", "UTC+11"), ("+12", "UTC+12")
    ]
    
    for tz_value, tz_text in timezones:
        builder.add(InlineKeyboardButton(
            text=tz_text,
            callback_data=f"set_timezone:{tz_value}"
        ))
    
    builder.add(InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_settings"))
    builder.adjust(3, 3, 3, 2)
    return builder.as_markup()
