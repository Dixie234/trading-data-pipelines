CREATE TABLE IF NOT EXISTS finance_pipeline.public.historic_price (
    id SERIAL PRIMARY KEY,
    price_date DATE,
    price_open NUMERIC,
    price_high NUMERIC,
    price_low NUMERIC, 
    price_close NUMERIC,
    volume BIGINT,
    dividends NUMERIC,
    stock_splits NUMERIC,
    symbol TEXT
);