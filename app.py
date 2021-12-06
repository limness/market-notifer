
import asyncio
from aiogram import executor

from handlers import *
from dispatcher import dp

from websocket import launch


##################

if __name__ == "__main__":
    print("Websocket has been started!")
    loop = asyncio.get_event_loop()
    loop.create_task(launch())

    print("Bot has been started!")
    executor.start_polling(dp, skip_updates = False)
