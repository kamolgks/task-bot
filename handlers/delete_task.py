from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards import main_keyboard, confirm_delete
from database.database import Database
from config import MESSAGES

router = Router()


@router.callback_query(F.data.startswith("confirm_delete:"))
async def confirm_delete_task(callback: CallbackQuery, db: Database):
    task_id = int(callback.data.split(":")[1])
    user_id = callback.from_user.id

    task = await db.get_task(task_id, user_id)
    if not task:
        await callback.message.edit_text(MESSAGES["task_not_found"])
        await callback.answer()
        return

    description = f"📝 {task['description']}\n" if task["description"] else ""
    confirm_message = MESSAGES["confirm_delete"].format(
        name=task['name'],
        id=task['id'],
        date=task['date'],
        time=task['time'],
        description=description
    )

    if task["description"]:
        confirm_message += f"📝 {task['description']}\n"

    await callback.message.edit_text(
        confirm_message, reply_markup=confirm_delete(task_id), parse_mode="HTML"
    )

    await callback.answer("F")


@router.callback_query(F.data.startswith("delete_task:"))
async def delete_task(callback: CallbackQuery, db: Database):
    task_id = int(callback.data.split(":")[1])
    user_id = callback.from_user.id

    task = await db.get_task(task_id, user_id)

    if not task:
        await callback.message.edit_text("Задача не найдена или уже была удалена.")
        await callback.answer()
        return

    await db.delete_task(task_id, user_id)
    await callback.message.edit_text(MESSAGES["task_deleted"].format(name=task['name']))

    remaining_tasks = await db.get_tasks(user_id)

    if remaining_tasks:
        await callback.message.answer(
            MESSAGES["remaining_tasks"].format(count=len(remaining_tasks)),
            reply_markup=main_keyboard,
        )
    else:
        await callback.message.answer(
            MESSAGES["no_remaining_tasks"],
            reply_markup=main_keyboard,
        )

    await callback.answer("Задача успешно удалена!")
