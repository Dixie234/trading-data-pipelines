CREATE TABLE IF NOT EXISTS finance_pipeline.public.symbol_sentiment (
    id SERIAL PRIMARY KEY,
    symbol TEXT,
    sentiment_date DATE,
    change NUMERIC,
    sentiment_score NUMERIC
);