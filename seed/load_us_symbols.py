import finnhub

def load_us_symbols(cur, client:finnhub.Client) -> None:
    symbols = client.stock_symbols('US')

    for s in symbols:
        cur.execute("""
            INSERT INTO public.us_symbols (currency, description, display_symbol, figi, isin, mic, share_class_figi, symbol, symbol2, type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (symbol) DO NOTHING;
        """, (s["currency"], s["description"], s["displaySymbol"], s["figi"], s["isin"], s["mic"], s["shareClassFIGI"], s["symbol"], s["symbol2"], s["type"]))

    print(f"Inserted {len(symbols)} US symbols successfully.")