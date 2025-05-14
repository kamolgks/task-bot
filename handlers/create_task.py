import logging
import re

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from datetime import datetime
from fsm.task_state import CreateTaskStates
from keyboards import main_keyboard, cancel_keyboard
from database.database import Database
from config import MESSAGES

router = Router()
logger = logging.getLogger(__name__)


def is_valid_date(date_str):
    try:
        if not re.match(r"^\d{2}\.\d{2}\.\d{4}$", date_str):
            return False

        day, month, year = map(int, date_str.split("."))
        datetime(year, month, day)

        today = datetime.now().date()
        input_date = datetime(year, month, day).date()
        if input_date < today:
            return False

        return True
    except ValueError:
        return False


def is_valid_time(time_str):
    try:
        if not re.match(r"^\d{1,2}:\d{2}$", time_str):
            return False

        hours, minutes = map(int, time_str.split(":"))
        if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
            return False

        return True
    except ValueError:
        return False


@router.message(F.text == "📝 Создать задачу")
async def create_task_start(message: Message, state: FSMContext):
    await state.set_state(CreateTaskStates.waiting_for_name)
    await message.answer(MESSAGES["enter_task_name"], reply_markup=cancel_keyboard())


@router.message(CreateTaskStates.waiting_for_name)
async def process_task_name(message: Message, state: FSMContext):
    if len(message.text) > 100:
        await message.answer(MESSAGES["name_too_long"])
        return

    await state.update_data(name=message.text)
    await state.set_state(CreateTaskStates.waiting_for_desc)
    await message.answer(
        MESSAGES["enter_description"],
        reply_markup=cancel_keyboard(),
    )


@router.message(CreateTaskStates.waiting_for_desc)
async def process_task_description(message: Message, state: FSMContext):
    description = "" if message.text == "-" else message.text
    await state.update_data(description=description)
    await state.set_state(CreateTaskStates.waiting_for_date)
    await message.answer(
        MESSAGES["enter_date"],
        reply_markup=cancel_keyboard(),
    )


@router.message(CreateTaskStates.waiting_for_date)
async def process_task_date(message: Message, state: FSMContext):
    if not is_valid_date(message.text):
        await message.answer(MESSAGES["invalid_date"])
        return

    await state.update_data(date=message.text)
    await state.set_state(CreateTaskStates.waiting_for_time)
    await message.answer(
        MESSAGES["enter_time"],
        reply_markup=cancel_keyboard(),
    )


@router.message(CreateTaskStates.waiting_for_time)
async def process_task_time(message: Message, state: FSMContext, db: Database):
    if not is_valid_time(message.text):
        await message.answer(MESSAGES["invalid_time"])
        return

    data = await state.get_data()
    name = data.get("name")
    description = data.get("description", "")
    date = data.get("date")
    time = message.text

    user_id = message.from_user.id
    await db.add_task(user_id, name, description, date, time)

    await state.clear()
    await message.answer(
        MESSAGES["task_created"].format(
            name=name,
            date=date,
            time=time,
            description=description if description else '(без описания)'
        ),
        parse_mode="HTML",
        reply_markup=main_keyboard,
    )
