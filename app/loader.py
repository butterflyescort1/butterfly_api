import uvicorn

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from core.api import app
from data.config import token

default = DefaultBotProperties(parse_mode=ParseMode.HTML)
bot = Bot(
    token=token,
    default=default
)
dp = Dispatcher()

config = uvicorn.Config(app, host="0.0.0.0", port=8000)
server = uvicorn.Server(config)
