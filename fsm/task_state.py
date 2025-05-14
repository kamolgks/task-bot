from aiogram.fsm.state import StatesGroup, State

class CreateTaskStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_desc = State()
    waiting_for_date = State()
    waiting_for_time = State()

