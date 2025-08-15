import asyncio
import signal
import uvicorn

from tortoise import Tortoise

from core.api import app
from data.config import DATABASE_CONFIG


async def main() -> None:
    signal.signal(signal.SIGINT, lambda *_: ...)

    await Tortoise.init(DATABASE_CONFIG)
    await Tortoise.generate_schemas()

    config = uvicorn.Config(app)
    server = uvicorn.Server(config)
    await server.serve()

    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(main())
