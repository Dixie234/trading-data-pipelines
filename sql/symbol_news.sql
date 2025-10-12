CREATE TABLE IF NOT EXISTS finance_pipeline.public.symbol_news (
    id SERIAL PRIMARY KEY,
    category TEXT,
    news_datetime TIMESTAMPTZ,
    headline TEXT,
    news_id INT,
    image_url TEXT,
    related TEXT,
    source TEXT,
    summary TEXT,
    url TEXT,
    sentiment_score NUMERIC
);