from aiogram.fsm.state import StatesGroup, State


class AdminMakePost(StatesGroup):
    post_command = State()
    make_post = State()
    end_make_post = State()

class RegisterUser(StatesGroup):
    registration_email = State()

