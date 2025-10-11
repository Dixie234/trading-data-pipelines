from urllib.parse import urlparse
import finnhub
import psycopg2
import os

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

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

cur.execute("""
CREATE TABLE IF NOT EXISTS binance_symbols (
    id SERIAL PRIMARY KEY,
    symbol TEXT UNIQUE,
    display_symbol TEXT,
    description TEXT
);
""")

symbols = finnhub_client.crypto_symbols('BINANCE')

for s in symbols:
    cur.execute("""
        INSERT INTO binance_symbols (symbol, display_symbol, description)
        VALUES (%s, %s, %s)
        ON CONFLICT (symbol) DO NOTHING;
    """, (s["symbol"], s["displaySymbol"], s["description"]))

conn.commit()
cur.close()
conn.close()

print(f"Inserted {len(symbols)} Binance symbols successfully.")