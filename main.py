import os
import requests

from dotenv import load_dotenv
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
CRYPTO_NAME = {
    'Bitcoin': 'BTCUSDT',
    'Ethereum': 'ETHUSDT',
    'Doge': 'DOGEUSDT'
}

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(row_width=3)
    for crypto_name in CRYPTO_NAME.keys():
        item_button = KeyboardButton(crypto_name)
        markup.add(item_button)
    bot.send_message(message.chat.id, 'Привет🖐😃 Выбери криптовалюту', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in CRYPTO_NAME.keys())
def send_price(message):
    crypto_name = message.text
    ticker = CRYPTO_NAME[crypto_name]
    price = get_price_by_ticker(ticker)
    bot.send_message(message.chat.id, f'Курс {crypto_name} к USDT составляет {price}')

def get_price_by_ticker(ticker):
    url = 'https://api.binance.com/api/v3/ticker/price'
    responce = requests.get(url, params={
        'symbol': ticker
    })
    data = responce.json()
    return round(float(data['price']), 2)

bot.infinity_polling()