from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from keyboards import main_keyboard
from config import MESSAGES

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer_photo(
        photo="https://i.imgur.com/l7UJsDt.jpeg",
        caption=MESSAGES["start"].format(full_name=message.from_user.full_name),
        parse_mode="HTML",
        reply_markup=main_keyboard,
    )


@router.message(Command("help"))
async def help_(message: Message):
    await message.answer(MESSAGES["help"], parse_mode="HTML", reply_markup=main_keyboard)


@router.message(Command("cancel"))
@router.message(F.text == "❌ Отмена")
async def cancel(message: Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is not None:
        await state.clear()
        await message.answer(MESSAGES["cancel"], reply_markup=main_keyboard)
    else:
        await message.answer(MESSAGES["already_in_menu"], reply_markup=main_keyboard)


@router.callback_query(F.data == "cancel_action")
async def cancel_action(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()

    if current_state is not None:
        await state.clear()

    await callback.message.edit_text("Действие отменено.")
    await callback.message.answer(
        "Вы вернулись в главное меню.", reply_markup=main_keyboard
    )
    await callback.answer()
