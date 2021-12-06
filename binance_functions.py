
from binance import Client
from binance import ThreadedWebsocketManager
from binance import ThreadedDepthCacheManager

from excel_manager import ExcelManager


##################
# Binance API Connection

api_key = ""
api_secret = ""
client = Client(api_key, api_secret)

##################

async def get_ticker(token: str) -> {}:
    """Gets ticker of token"""
    ticker = client.get_ticker(symbol=token)
    return ticker

async def get_all_tokens() -> "":
    """Gets all token names from Binance and return these as red string"""
    tokens_list = ' '.join([currency['symbol'] for currency in client.get_all_tickers()[:50]])
    return tokens_list

async def get_daily_candles(token: str) -> []:
    """Gets all candles for the last day"""
    candles_binance = client.get_historical_klines(
              token,
              Client.KLINE_INTERVAL_1MINUTE,
              "29 Oct, 2021",
              "30 Oct, 2021",
          )
    return candles_binance

async def generate_graphic(token: str) -> bool:
    """A method for generating a graph in Excel"""
    try:
        candles_binance = await get_daily_candles(token)
        excel = ExcelManager(token, [float(candle[4]) for candle in candles_binance])
        return True
    except Exception as ex:
        print(ex)
        return False
