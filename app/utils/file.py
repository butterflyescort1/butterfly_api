import hashlib
import json

from aiogram.types import FSInputFile

from database.requests import File
from loader import bot


def _get_checksum(path: str) -> str:
    with open(path, "rb") as file:
        return hashlib.md5(file.read()).hexdigest()


def _get_hash(checksum: str) -> str:
    data = {
        "checksum": checksum,
        "bot_id": bot.id
    }
    return hashlib.md5(json.dumps(data).encode("utf-8")).hexdigest()


async def get_file(path: str) -> str | FSInputFile:
    checksum = _get_checksum(path)
    data_hash = _get_hash(checksum)

    file = File(data_hash)
    if not await file.file_exists():
        return FSInputFile(path)
    
    file_id = await file.get_file_id()
    return file_id


async def upload_file(path: str, file_id: str):
    checksum = _get_checksum(path)
    data_hash = _get_hash(checksum)
    file = File(data_hash)

    if not await file.file_exists():
        await file.create_file(file_id)
