import asyncio

from tortoise import Tortoise

from data.config import DATABASE_CONFIG
from handlers import start_handler
from loader import bot, dp, server


async def main() -> None:
    await Tortoise.init(DATABASE_CONFIG)
    await Tortoise.generate_schemas()

    dp.include_router(start_handler.router)

    await bot.delete_webhook(drop_pending_updates=True)

    tasks = [
        asyncio.create_task(dp.start_polling(bot)),
        asyncio.create_task(server.serve())
    ]

    bot_ = await bot.get_me()
    print(f"[*] Telegram-Bot (@{bot_.username}) has been launched successfully!")

    await asyncio.gather(*tasks)

    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(main())
