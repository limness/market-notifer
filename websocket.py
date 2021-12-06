
import json
import time
import traceback
import websockets
import operator
import random

from aiogram.types import ParseMode

from dispatcher import dp, bot
from settings import Settings


async def unsubscribe(ws, topic: str):
    req_msg = {
        "method": "UNSUBSCRIBE",
        "params":
        [
            topic,
        ],
        "id": 312
    }
    await ws.send(json.dumps(req_msg))

async def subscribe(ws, topic: str):
    req_msg = {
        "method": "SUBSCRIBE",
        "params":
        [
            topic,
        ],
        "id": 312
    }
    await ws.send(json.dumps(req_msg))

async def consumer_handler(ws):
    """Processor of incoming messages from
    the exchange via a web socket"""
    async for msg in ws:
        # All messages come in string format, convert it to json
        msg = json.loads(msg)

        # Make sure that the incoming message is in a list format
        # and that the user has enabled push notifications
        if isinstance(msg, list) and Settings.get_top_alert:
            # First, let's throw out all unnecessary things from the resulting array
            msg = [{'Token': ticker['s'], 'Delta': float(ticker['P'])} for ticker in msg]

            # Let's sort the current delta of decline in ascending order
            # We need to get the smallest drop percentage
            msg.sort(key=operator.itemgetter('Delta'))
            # To demonstrate how the websocket works,
            # 20 tokens with the biggest drop is enough for us
            msg = msg[:20]

            # Choose any token from the list of the biggest drops of the day
            token_index = random.randrange(0, 19)

            answer = f"<b>{msg[token_index]['Token']} за последние "
            answer += f"сутки упал на {-msg[token_index]['Delta']}%! 🔥</b>\n"
            answer += f"Пора открывать новый ордер на покупку!"

            await bot.send_message(
                      chat_id = 867690422,
                      text = answer,
                      parse_mode = ParseMode.HTML,
                  )

            time.sleep(1.5)

async def launch():
    async with websockets.connect('wss://stream.binance.com:9443/ws') as ws:
        print('Websocket running...')

        # Subscribing to receive messages by tickers of all tokens
        await subscribe(ws, "!ticker@arr")

        # Set the handler for messages from Binance
        await consumer_handler(ws)
