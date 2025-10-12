from typing import List
import pandas as pd
import yfinance as yf
from psycopg2.extras import execute_values

column_mappings = {
    "Date": "price_date",
    "Open": "price_open",
    "High": "price_high",
    "Low": "price_low", 
    "Close": "price_close",
    "Volume": "volume",
    "Dividends": "dividends",
    "Stock Splits": "stock_splits",
    "symbol": "symbol"
}

def load_historic_stocks(cur, symbols:List[str]) -> None:
    dfs = []
    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1y")
        data["symbol"] = symbol
        data["Date"] = data.index.date
        dfs.append(data)

    df = pd.concat(dfs)
    df = df.rename(columns=column_mappings)
    data = [tuple(x) for x in df.to_numpy()]
    cols = ', '.join(df.columns)
    sql = f"INSERT INTO public.historic_price ({cols}) VALUES %s"
    execute_values(cur, sql, data)

    print(f"Inserted {len(data)} historical stock rows for 1 year successfully.")
