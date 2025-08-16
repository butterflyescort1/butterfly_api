from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from data.config import root_path, VIDEO_PATH
from html import escape
from typing import Optional

from data.config import messages, settings
from data.states import CityState
from database.requests import User
from keyboards.reply_keyboards import StartKeyboard
from utils.file import get_file, upload_file

router = Router()


@router.message(CommandStart())
async def get_start_command_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id

    user_data = await state.get_data()
    await state.clear()

    message_id: Optional[int] = user_data.get("message_id")
    if message_id is not None:
        try:
            await message.bot.delete_message(
                chat_id=user_id,
                message_id=message_id
            )
        except TelegramBadRequest:
            ...

    if await User(user_id).user_exists():
        video_path = root_path / VIDEO_PATH
        video = await get_file(video_path)

        user_name = escape(" ".split(list(filter(lambda name: name is not None, message.from_user.first_name, message.from_user.last_name))))

        sent_message = await message.answer_video(
            video=video,
            caption=messages["startMessage"].format(name=user_name),
            reply_markup=StartKeyboard(settings["butterflyURL"], user_id).get_start_keyboard()
        )
        await upload_file(video_path, sent_message.video.file_id)
        return
    
    sent_message = await message.answer(messages["enterCityMessage"])
    await state.update_data(message_id=sent_message.message_id)
    await state.set_state(CityState.city)


@router.message(
    F.text,
    CityState.city
)
async def get_city_text_message_handler(message: Message, state: FSMContext):
    await state.clear()

    city = message.text.capitalize()

    await User(message.from_user.id).create_user(city)

    await get_start_command_handler(message, state)
