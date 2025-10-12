import asyncio
import datetime
from datetime import date
from typing import List
from dateutil.relativedelta import relativedelta

import aiohttp
import finnhub
import nltk
import nest_asyncio
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from newspaper import Article
import pandas as pd

nltk.download("vader_lexicon", quiet=True)

async def fetch_article(session:aiohttp.ClientSession, url):
    try:
        async with session.get(url) as response:
            html = await response.text()
            article = Article(url="")
            article.set_html(html)
            article.parse()
            return article.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None
    
async def fetch_with_retries(session, url, retries=2):
    for attempt in range(retries + 1):
        text = await fetch_article(session, url)
        if text:
            return text
        await asyncio.sleep(1 + attempt)  # backoff
    return None

async def process_article(analyzer:SentimentIntensityAnalyzer, session, obj):
    url = obj.get("url")
    text = await fetch_with_retries(session, url)
    if text:
        sentiment = analyzer.polarity_scores(text)
        obj["sentiment"] = sentiment["compound"]
    else:
        obj["sentiment"] = None
    return obj

async def analyze_articles(analyzer, url_objects, concurrency=10):
    connector = aiohttp.TCPConnector(limit=concurrency)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [process_article(analyzer, session, obj) for obj in url_objects]
        results = await asyncio.gather(*tasks)
    return results

def analyze_articles_sync(analyzer, url_objects, concurrency=10):
    """
    Wrapper to run the asynchronous sentiment analysis from synchronous code.
    Returns the list of URL objects with sentiment data.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        nest_asyncio.apply()
        results = loop.run_until_complete(analyze_articles(analyzer, url_objects, concurrency))
    else:
        results = asyncio.run(analyze_articles(analyzer, url_objects, concurrency))

    return results

def load_symbol_news(cur, client: finnhub.Client, symbols:List[str]) -> None:
    today = date.today()
    one_year_ago = today - relativedelta(years=1)
    news_inserted = 0
    analyzer = SentimentIntensityAnalyzer()

    #dfs = []
    for symbol in symbols:
        news = client.company_news(symbol, _from=one_year_ago, to=today)
        news_plus_sentiment = analyze_articles_sync(analyzer, news)
        for article in news_plus_sentiment:
            cur.execute("""
                INSERT INTO public.symbol_news (category, news_datetime, headline, news_id, image_url, related, source, summary, url, sentiment_score)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", (
                article["category"], 
                datetime.datetime.fromtimestamp(article["datetime"]), 
                article["headline"], 
                article["id"], 
                article["image"], 
                article["related"], 
                article["source"], 
                article["summary"], 
                article["url"],
                article["sentiment"])
            )
            news_inserted += 1
        #dfs.append(pd.DataFrame(news_plus_sentiment))
        print(f"Inserted news data over the last year for symbol {symbol} successfully.")

    #df = pd.concat(dfs)
    print(f"Inserted {news_inserted} news articles successfully.")

