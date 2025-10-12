CREATE TABLE IF NOT EXISTS finance_pipeline.public.binance_symbols (
    id SERIAL PRIMARY KEY,
    symbol TEXT UNIQUE,
    display_symbol TEXT,
    description TEXT
);