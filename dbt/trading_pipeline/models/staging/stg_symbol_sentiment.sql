SELECT
    us.symbol,
    news_datetime::DATE AS sentiment_date,
    AVG(sn.sentiment_score) AS daily_sentiment_score
FROM {{ source('raw_data', 'symbol_news') }} sn
JOIN {{ source('raw_data', 'us_symbols')}} us ON us.symbol = sn.related
GROUP BY
    us.symbol,
    news_datetime::DATE