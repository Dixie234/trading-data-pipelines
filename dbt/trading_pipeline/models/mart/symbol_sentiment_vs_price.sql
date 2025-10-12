-- depends_on: {{ ref('stg_symbol_sentiment') }}

WITH price_diff AS
(
    SELECT
        s.symbol,
        s.sentiment_date,
        s.daily_sentiment_score,
        h.price_open - h.price_close AS price_diff
    FROM {{ ref('stg_symbol_sentiment')}} s
    JOIN {{ source('raw_data', 'historic_price')}} h ON h.symbol = s.symbol
                                                    AND h.price_date = s.sentiment_date
),
price_diff_range AS
(
    SELECT
        symbol,
        sentiment_date,
        daily_sentiment_score,
        price_diff,
        MAX(price_diff) OVER (PARTITION BY symbol ORDER BY (SELECT NULL)) AS max_diff, 
        MIN(price_diff) OVER (PARTITION BY symbol ORDER BY (SELECT NULL)) AS min_diff
    FROM price_diff
)
SELECT
    symbol,
    sentiment_date,
    daily_sentiment_score,
    2 * ((price_diff - min_diff) / NULLIF((max_diff - min_diff), 0)) - 1 AS price_change
FROM price_diff_range