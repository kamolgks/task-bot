from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards import main_keyboard, tasks_keyboard, task_actions
from database.database import Database
from config import MESSAGES

router = Router()


@router.message(F.text == "📋 Мои задачи")
async def show_all_tasks(message: Message, db: Database):
    user_id = message.from_user.id
    tasks = await db.get_tasks(user_id)
    if not tasks:
        await message.answer(
            MESSAGES["no_tasks"],
            reply_markup=main_keyboard,
        )
        return

    await message.answer(
        MESSAGES["all_tasks_header"].format(count=len(tasks)),
        reply_markup=tasks_keyboard(tasks),
        parse_mode="HTML",
    )


@router.message(F.text == "📅 Задачи на сегодня")
async def show_today_tasks(message: Message, db: Database):
    user_id = message.from_user.id
    tasks = await db.get_today_tasks(user_id)
    if not tasks:
        await message.answer(
            MESSAGES["no_tasks_today"],
            reply_markup=main_keyboard,
        )
        return

    await message.answer(
        MESSAGES["today_tasks_header"].format(count=len(tasks)),
        reply_markup=tasks_keyboard(tasks),
        parse_mode="HTML",
    )


@router.message(F.text == "🔮 Будущие задачи")
async def show_future_tasks(message: Message, db: Database):
    user_id = message.from_user.id
    tasks = await db.get_future_tasks(user_id)
    if not tasks:
        await message.answer(
            MESSAGES["no_future_tasks"],
            reply_markup=main_keyboard,
        )
        return

    tasks_by_date = {}
    for task in tasks:
        date = task["date"]
        if date not in tasks_by_date:
            tasks_by_date[date] = []
        tasks_by_date[date].append(task)
        message_text = MESSAGES["future_tasks_header"].format(count=len(tasks))
    for date, date_tasks in tasks_by_date.items():
        message_text += f"📅 <b>{date}:</b>\n"
        for task in date_tasks:
            message_text += f"• {task['time']} - {task['name']}\n"
        message_text += "\n"

    message_text += "Выберите задачу для просмотра подробностей:"
    await message.answer(
        message_text, reply_markup=tasks_keyboard(tasks), parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("view_task:"))
async def show_task_details(callback: CallbackQuery, db: Database):
    task_id = int(callback.data.split(":")[1])
    user_id = callback.from_user.id

    task = await db.get_task(task_id, user_id)
    if not task:
        await callback.message.edit_text(MESSAGES["task_not_found"])
        await callback.answer()
        return
    task_details = MESSAGES["task_details"].format(
        name=task['name'],
        date=task['date'],
        time=task['time'],
        description=f"\n📝 <b>Описание:</b>\n{task['description']}\n" if task["description"] else "\n📝 <b>Описание:</b> не указано\n",
        created_at=task['created_at']
    )
    await callback.message.edit_text(
        task_details, reply_markup=task_actions(task_id), parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_tasks")
async def back_to_tasks_list(callback: CallbackQuery, db: Database):
    user_id = callback.from_user.id
    tasks = await db.get_tasks(user_id)
    if not tasks:
        await callback.message.edit_text(MESSAGES["no_tasks"])
        await callback.answer()
        return

    await callback.message.edit_text(
        text=MESSAGES["all_tasks_header"].format(count=len(tasks)),
        reply_markup=tasks_keyboard(tasks),
        parse_mode="HTML",
    )
