import logging
import os

from aiogram import Bot, Dispatcher


##################

logging.basicConfig(filename = "logs/telegram_log.txt", level = logging.INFO)

# You can use 5099140563:AAHk0IGK-58J3koeoAWifXFP6069rSoyxyw for a test
TOKEN = os.getenv("BOT_BINANCE")

bot = Bot(token = TOKEN)
dp = Dispatcher(bot)

##################
