import logging

from aiogram import Bot, Dispatcher


##################

logging.basicConfig(filename = "logs/telegram_log.txt", level = logging.INFO)

TOKEN = "5099140563:AAHk0IGK-58J3koeoAWifXFP6069rSoyxyw"

bot = Bot(token = TOKEN)
dp = Dispatcher(bot)

##################
