import json

import requests
from scipy.stats import pearsonr

# URL для получения последней цены фьючерса на ETHUSDT
ETHUSDT_URL = 'https://fapi.binance.com/fapi/v1/ticker/price?symbol=ETHUSDT'
# URL для получения последней цены фьючерса на BTCUSDT
BTC_PRICE_URL = 'https://fapi.binance.com/fapi/v1/ticker/price?symbol=BTCUSDT'

# Параметр для проверки изменения цены на 1%
CHANGE_THRESHOLD = 1 / 100

# Массивы для хранения цен BTCUSDT и ETHUSDT
btc_prices = []
eth_prices = []


def get_current_btc_price():
    """Функция для получения текущей цены фьючерса BTCUSDT"""
    response = requests.get(BTC_PRICE_URL)
    data = json.loads(response.text)
    return float(data['price'])


def get_current_eth_price():
    """Функция для получения текущей цены фьючерса ETHUSDT"""
    response = requests.get(ETHUSDT_URL)
    data = json.loads(response.text)
    return float(data['price'])


def calculate_correlation():
    """Функция для расчета корреляции между ценами ETHUSDT и BTCUSDT"""
    correlation, _ = pearsonr(eth_prices, btc_prices)
    return correlation


def check_price_change():
    """Функция для проверки изменения цены на 1% за последние 60 минут"""
    eth_price = get_current_eth_price()
    eth_prices.append(eth_price)
    btc_price = get_current_btc_price()
    btc_prices.append(btc_price)

    if len(eth_prices) > 60:
        eth_prices.pop(0)
    if len(btc_prices) > 60:
        btc_prices.pop(0)

    if len(eth_prices) == 60:
        correlation = calculate_correlation()
        if abs(correlation) < 0.9:
            min_eth_price = min(eth_prices)
            max_eth_price = max(eth_prices)
            price_change = (max_eth_price - min_eth_price) / min_eth_price * 100
            if price_change >= CHANGE_THRESHOLD:
                print(f"ETHUSDT futures price: {eth_price:.2f}")


if __name__ == "__main__":
    while True:
        check_price_change()
