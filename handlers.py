import asyncio

from datetime import datetime
from aiogram import types
from aiogram.types import ParseMode

from dispatcher import dp, bot

from binance_functions import get_all_tokens
from binance_functions import get_daily_candles
from binance_functions import get_ticker
from binance_functions import generate_graphic

from settings import Settings

##################

""" Commands

    /help /start - Посмотреть список доступных команд
    /tokens_list - Список токенов на бинансе
    /form_graphic - Сформировать график
    /get_top - Получать уведомления по выгодным парам

"""
@dp.message_handler(commands = ["start", "help"], commands_prefix = "!/")
async def cmd_start(message: types.Message):
    answer = "Привет, видимо ты новенький. "
    answer += "Давай представлюсь, Я — <b>парсер одного программиста</b>, который хочет получить работу, "
    answer += "созданный для получения самых актуальных данных с биржи 🔶 <b>Binance</b> с целью торговли.\n\n"
    answer += "<b>Давай покажу, что я умею:</b>\n\n"
    answer += "<i>Я могу</i> изучить список всех доступных токенов и показать тебе, что сейчас на пике роста. "
    answer += "Данные будут передаваться по\n 👁‍🗨 веб-сокету, поэтому ты начнешь получать постоянные уведомления. "
    answer += "Введи команду /get_top\n\n"
    answer += "<i>Я могу</i> сформировать отчет по тренду определенного токена и выводить его в <b>XLS/XLSX</b> формате. "
    answer += "Введи команду /form_graphic [имя токена]\n\n"
    answer += "Для просмотра доступных токенов используйте команду /tokens_list"

    await bot.send_message(
              chat_id = message.from_user.id,
              text = answer,
              parse_mode = ParseMode.HTML,
          )

@dp.message_handler(commands = ["tokens_list"], commands_prefix = "!/")
async def cmd_tokens_list(message: types.Message):
    answer = "<b>🌪 Формирую список...</b>"
    await bot.send_message(
              chat_id = message.from_user.id,
              text = answer,
              parse_mode = ParseMode.HTML,
          )

    answer = "<b>📃 Список доступных токенов:</b>\n\n"
    answer += await get_all_tokens()

    await bot.send_message(
              chat_id = message.from_user.id,
              text = answer,
              parse_mode = ParseMode.HTML,
          )

@dp.message_handler(commands = ["get_top"], commands_prefix = "!/")
async def cmd_get_top(message: types.Message):
    if not Settings.get_top_alert:
        answer = "<b>🔸 В ближайшее время ты начнешь получать уведомления</b> "
        answer += "Используй повторно команду /get_top для отключения пуша уведомлений"
    else:
        answer = "<b>🔺 Ты отключил пуш уведомлений, теперь можешь спать спокойно.</b> "
        answer += "Однако с этого момента придется самому следить за движением цены"

    Settings.user_id = message.from_user.id
    Settings.get_top_alert = not Settings.get_top_alert

    await bot.send_message(
              chat_id = message.from_user.id,
              text = answer,
              parse_mode = ParseMode.HTML,
          )

@dp.message_handler(commands = ["form_graphic"], commands_prefix = "!/")
async def cmd_form_graphic(message: types.Message):
    # Args list
    arguments = message.get_args().split(" ")

    if len(arguments) != 1 or arguments[0].strip() == '':
        answer = "Аргументы не совпадают"
        return await bot.send_message(
                  chat_id = message.from_user.id,
                  text = answer,
                  parse_mode = ParseMode.HTML,
              )

    answer = "<b>🌪 Формирую график токена...</b>"
    await bot.send_message(
              chat_id = message.from_user.id,
              text = answer,
              parse_mode = ParseMode.HTML,
          )

    # Generate general information and output it to the user
    ticker = await get_ticker(arguments[0])
    answer = f"Информация по <b>{arguments[0]}</b> за последние сутки:\n\n"
    answer += f"Текущая цена: <b>{round(float(ticker['bidPrice']), 2)}</b> 📌\n"
    answer += f"Дельта изменения: <b>{round(float(ticker['priceChangePercent']), 2)}%</b>\n"
    answer += f"Общий объем: <b>{round(float(ticker['volume']), 2)} BTC</b>\n\n"
    answer += "📊 Более подробную информацию <b>по изменению цены</b>\n"
    answer += "за сутки можно увидеть в файлике ниже:"

    await bot.send_message(
              chat_id = message.from_user.id,
              text = answer,
              parse_mode = ParseMode.HTML,
          )

    if await generate_graphic(arguments[0]):
        await bot.send_document(
                  message.from_user.id,
                  open("charts.xlsx", 'rb')
              )
