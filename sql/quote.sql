CREATE TABLE IF NOT EXISTS finance_pipeline.public.quote (
    id SERIAL PRIMARY KEY,
    symbol TEXT,
    quote_timestamp TIMESTAMPTZ,
    current_price NUMERIC,
    change NUMERIC,
    percent_change NUMERIC,
    price_high NUMERIC,
    price_low NUMERIC,
    price_open NUMERIC,
    previous_price_close NUMERIC
);