SELECT
    symbol,
    TO_CHAR(price_date, 'Mon-yy') as price_date,
    AVG(price_close) as price
FROM {{ source('raw_data', 'historic_price')}}
GROUP BY symbol, TO_CHAR(price_date, 'Mon-yy')