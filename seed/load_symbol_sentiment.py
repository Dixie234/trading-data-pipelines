from datetime import date
from typing import List
from dateutil.relativedelta import relativedelta
import finnhub


def load_symbol_sentiment(cur, client: finnhub.Client, symbols:List[str]) -> None:
    today = date.today()
    one_year_ago = today - relativedelta(years=1)
    sentiments_inserted = 0
    for symbol in symbols:
        sentiments = client.stock_insider_sentiment(symbol, _from=one_year_ago, to=today)
        for sentiment in sentiments["data"]:
            cur.execute("""
                INSERT INTO public.symbol_sentiment (symbol, sentiment_date, change, sentiment_score)
                VALUES (%s, %s, %s, %s);
            """, (sentiment["symbol"], date(sentiment["year"], sentiment["month"], 1), sentiment["change"], sentiment["mspr"]))
            sentiments_inserted += 1

        print(f"Inserted sentiment data over the last year for symbol {symbol} successfully.")

    print(f"Inserted {sentiments_inserted} sentiment scores successfully.")

