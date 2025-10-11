CREATE TABLE finance_pipeline.public.live_prices (
    id SERIAL PRIMARY KEY,
    symbol TEXT,
    price NUMERIC,
    timestamp TIMESTAMPTZ
);