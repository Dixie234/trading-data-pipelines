import datetime
import time
from typing import List
import finnhub

def load_quotes(cur, client:finnhub.Client, symbols:List[str]) -> None:
    quotes_inserted = 0
    quote_timestamp = datetime.datetime.fromtimestamp(time.time())

    for symbol in symbols:
        quote = client.quote(symbol)
        cur.execute("""
            INSERT INTO public.quote (symbol, quote_timestamp, current_price, change, percent_change, price_high, price_low, price_open, previous_price_close)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (symbol, quote_timestamp, quote["c"], quote["d"], quote["dp"], quote["h"], quote["l"], quote["o"], quote["pc"]))
        quotes_inserted += 1

        print(f"Inserted quote data for symbol {symbol} successfully.")

    print(f"Inserted {quotes_inserted} quotes successfully.")
