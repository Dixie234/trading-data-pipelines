import os
import time
from urllib.parse import urlparse
from dotenv import load_dotenv
import finnhub
import websocket, json, psycopg2, datetime

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
connection_string = urlparse(DATABASE_URL)
conn = psycopg2.connect(
    dbname=connection_string.path[1:],
    user=connection_string.username,
    password=connection_string.password,
    host=connection_string.hostname,
    port=5432
)
cur = conn.cursor()

with open("settings.json", "r") as s:
    settings = json.load(s)

SYMBOL_LIST = settings["SYMBOL_LIST"]

last_update = 0
def on_message(ws:websocket.WebSocketApp, message:str) -> None:
    global last_update
    now = time.time()
    if now - last_update < 1:
        return
    last_update = now

    data = json.loads(message)
    if 'data' in data:
        for entry in data['data']:
            symbol = entry['s']
            price = entry['p']
            timestamp = datetime.datetime.fromtimestamp(entry['t']/1000)
            cur.execute(
                "INSERT INTO live_prices (symbol, price, timestamp) VALUES (%s, %s, %s)",
                (symbol, price, timestamp)
            )
            conn.commit()

def on_open(ws:websocket.WebSocketApp) -> None:
    for symbol in SYMBOL_LIST:
        ws.send(json.dumps({"type": "subscribe", "symbol": symbol}))

def on_error(ws, error):
    print(f"WebSocket error: {error}")

def on_close(ws):
    print(f"WebSocket closed")

def main():
    api_key = os.getenv("FINNHUB_API_KEY")

    #finnhub_client = finnhub.Client(api_key=api_key)
    #print(finnhub_client.crypto_symbols('BINANCE'))
    #print(finnhub_client.stock_symbols('US'))

    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        f"wss://ws.finnhub.io?token={api_key}",
        on_message=on_message,
        on_open=on_open,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()

if __name__ == "__main__":
    main()

