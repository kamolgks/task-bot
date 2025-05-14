from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from keyboards.inline import settings_keyboard, timezone_keyboard
from database.database import Database
from config import MESSAGES

router = Router()

class SettingsState(StatesGroup):
    waiting_for_timezone = State()

@router.message(F.text == "⚙️ Настройки")
async def show_settings(message: Message):
    await message.answer(
        MESSAGES["settings_menu"],
        reply_markup=settings_keyboard()
    )

@router.callback_query(F.data == "change_timezone")
async def change_timezone(callback: CallbackQuery):
    await callback.message.edit_text(
        MESSAGES["choose_timezone"],
        reply_markup=timezone_keyboard()
    )

@router.callback_query(F.data.startswith("set_timezone:"))
async def set_timezone(callback: CallbackQuery, db: Database):
    timezone = callback.data.split(":")[1]
    user_id = callback.from_user.id
    
    await db.set_user_timezone(user_id, timezone)
    await callback.message.edit_text(
        MESSAGES["timezone_set"].format(timezone=timezone),
        reply_markup=settings_keyboard()
    )
    await callback.answer(MESSAGES["timezone_success"])

@router.callback_query(F.data == "back_to_settings")
async def back_to_settings(callback: CallbackQuery):
    await callback.message.edit_text(
        MESSAGES["settings_menu"],
        reply_markup=settings_keyboard()
    )
    await callback.answer()
