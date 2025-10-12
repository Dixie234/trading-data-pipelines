import json
import os
from urllib.parse import urlparse

import finnhub
import psycopg2

from load_crypto_symbols import load_crypto_symbols
from load_quotes import load_quotes
from load_us_symbols import load_us_symbols
from load_historic_stock_price import load_historic_stocks
from load_symbol_news import load_symbol_news
from load_symbol_sentiment import load_symbol_sentiment


def create_db_conn(conn_string:str):
    connection_string = urlparse(conn_string)
    conn = psycopg2.connect(
        dbname=connection_string.path[1:],
        user=connection_string.username,
        password=connection_string.password,
        host=connection_string.hostname,
        port=5432
    )
    return conn

def create_finn_app_client(api_key:str) -> finnhub.Client:
    finnhub_client = finnhub.Client(api_key=api_key)
    return finnhub_client

def main():
    with open("settings.json", "r") as s:
        settings = json.load(s)

    BATCH_SYMBOLS = settings["BATCH_SYMBOLS"]
    DATABASE_URL = os.getenv("DATABASE_URL")
    FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
    
    conn = create_db_conn(DATABASE_URL)
    finn_client = create_finn_app_client(FINNHUB_API_KEY)

    with create_db_conn(DATABASE_URL) as conn:
        cur = conn.cursor()
        load_crypto_symbols(cur, finn_client)
        load_us_symbols(cur, finn_client)
        load_quotes(cur, finn_client, BATCH_SYMBOLS)
        load_historic_stocks(cur, BATCH_SYMBOLS)
        load_symbol_news(cur, finn_client, BATCH_SYMBOLS)
        load_symbol_sentiment(cur, finn_client, BATCH_SYMBOLS)
        cur.close()

if __name__ == "__main__":
    main()