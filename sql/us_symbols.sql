CREATE TABLE IF NOT EXISTS finance_pipeline.public.us_symbols (
    id SERIAL PRIMARY KEY,
    currency TEXT,
    description TEXT,
    display_symbol TEXT,
    figi TEXT,
    isin TEXT,
    mic TEXT,
    share_class_figi TEXT,
    symbol TEXT UNIQUE,
    symbol2 TEXT,
    type TEXT
);