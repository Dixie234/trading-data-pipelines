import finnhub


def load_crypto_symbols(cur, client:finnhub.Client) -> None:
    symbols = client.crypto_symbols('BINANCE')

    for s in symbols:
        cur.execute("""
            INSERT INTO binance_symbols (symbol, display_symbol, description)
            VALUES (%s, %s, %s)
            ON CONFLICT (symbol) DO NOTHING;
        """, (s["symbol"], s["displaySymbol"], s["description"]))

    print(f"Inserted {len(symbols)} Binance symbols successfully.")


