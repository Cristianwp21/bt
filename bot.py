from binance.client import Client
import pandas as pd
import numpy as np
import time
from telegram import Bot
name: bot-env
channels:
  - defaults
dependencies:
  - python=3.9
  - python-binance=1.0.16
  - pycryptodome=3.18.0
  - requests=2.31.0
  - pandas=2.0.3


# Configurações da API da Binance
API_KEY = "WGppsqHCM893qJD9IeAx20SzEw5Ewdb1IzUBzS0r9gHZRiAP8LPbtK3l1RWqwQKZ"
API_SECRET = "QrPiz5LYJS20oRJZb3JX7W5Ts7Bd7WrZ36PlG389JaHrfxHv0Th0Jd0uTZd345cB"

client = Client(API_KEY, API_SECRET)

# Configurações de mercado
SYMBOL = "BTCUSDT"  # Par de negociação
INTERVAL = Client.KLINE_INTERVAL_15MINUTE  # Intervalo de 15 minutos

# Configurações do Telegram
TELEGRAM_TOKEN = "7676787815:AAHLOCqbmuQgJN8NDgxvsgnyoH_nMhWCbyM"
CHAT_ID = "1234567890"

# Função para enviar alertas no Telegram
def enviar_alerta(mensagem):
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=mensagem)

# Função para calcular o RSI
def calculate_rsi(data, period=14):
    close_prices = pd.Series([float(kline[4]) for kline in data])  # Preços de fechamento
    delta = close_prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(0).tolist()  # Retorna o RSI como lista

# Função para buscar dados de mercado
def get_market_data(symbol, interval, limit=100):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    return klines

# Função para pegar todos os pares de negociação
def get_all_pairs():
    exchange_info = client.get_exchange_info()
    symbols = [s['symbol'] for s in exchange_info['symbols'] if s['status'] == 'TRADING']
    return symbols

# Função para enviar alertas via Telegram (caso queira implementar)
def enviar_alerta(mensagem, token, chat_id):
    bot = Bot(token=token)
    bot.send_message(chat_id=chat_id, text=mensagem)

# Função principal do bot
def run_bot():
    # Pega todos os pares de moedas disponíveis na Binance
    pairs = get_all_pairs()
    
    while True:
        for symbol in pairs:
            try:
                # Busca os dados de mercado para o par atual
                market_data = get_market_data(symbol, INTERVAL)
                rsi = calculate_rsi(market_data)

                # Exemplo de análise: RSI abaixo de 30 (sobrevendido)
                if rsi[-1] < 30:
                    print(f"Alerta: RSI de {symbol} está sobrevendido ({rsi[-1]:.2f})")
                    # Enviar alerta via Telegram aqui, se configurado

                # Pausa antes da próxima verificação
                time.sleep(60)  # Aguarda 1 minuto

            except Exception as e:
                print(f"Erro ao verificar o par {symbol}: {e}")
                time.sleep(60)  # Aguarda 1 minuto antes de tentar novamente

if __name__ == "__main__":
    run_bot()
