import json
import os
import time
from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

CONN = os.getenv("DATABASE_URL")
engine = create_engine(CONN)

with open("settings.json", "r") as s:
    settings = json.load(s)

STREAM_SYMBOLS = settings["STREAM_SYMBOLS"]
BATCH_SYMBOLS = settings["BATCH_SYMBOLS"]

st.set_page_config(page_title="Stock Dashboard", layout="wide")
st.title("📈 Stock Dashboard")

placeholder = st.empty()

st.cache_data(ttl=1)
def load_live_data(symbol):
    query = f"""
    SELECT lp.price, bs.description
    FROM public.live_prices lp
    JOIN public.binance_symbols bs ON bs.symbol = lp.symbol
    WHERE lp.symbol = '{symbol}'
    ORDER BY lp.timestamp DESC LIMIT 1
    """
    df = pd.read_sql(query, engine)
    return df

def load_sentiment_data(symbol):
    query = f"""
    SELECT
        TO_CHAR(sentiment_date, 'DD-Mon') as sentiment_date, 
        COALESCE(daily_sentiment_score, 0) as daily_sentiment_score, 
        price_change
    FROM public.symbol_sentiment_vs_price
    WHERE symbol = '{symbol}'
    ORDER BY sentiment_date
    """
    df = pd.read_sql(query, engine)
    return df

def load_historic_data(symbol):
    query = f"""
    SELECT
        price_date, 
        price
    FROM public.price_by_month
    WHERE symbol = '{symbol}'
    ORDER BY price_date
    """
    df = pd.read_sql(query, engine)
    return df

def load_quote_data(symbol):
    query = f"""
    SELECT
        current_price, 
        change,
        percent_change,
        price_high,
        price_low
    FROM public.quote
    WHERE symbol = '{symbol}'
    LIMIT 1
    """
    df = pd.read_sql(query, engine)
    return df

def styled_number(value, size=16):
    color = "green" if value > 0 else "red" if value < 0 else "black"
    sign = "+" if value > 0 else "−" if value < 0 else ""
    return f"<span style='color:{color}; font-size:{size}px;'>{sign}{abs(value):.2f}</span>"

st.session_state.data = {}
for symbol in STREAM_SYMBOLS:
    st.session_state.data[symbol] = load_live_data(symbol)

st.session_state.sentiment_data = {}
st.session_state.historic_data = {}
st.session_state.quote_data = {}
for symbol in BATCH_SYMBOLS:
    st.session_state.sentiment_data[symbol] = load_sentiment_data(symbol)
    st.session_state.historic_data[symbol] = load_historic_data(symbol)
    st.session_state.quote_data[symbol] = load_quote_data(symbol)

selected_symbol = st.selectbox("Select a symbol:", BATCH_SYMBOLS)

#todays prices
quote_column_names = st.session_state.quote_data[selected_symbol].columns
quote_columns = st.columns(len(st.session_state.quote_data[selected_symbol].columns))
for i, column in enumerate(quote_columns):
    column_name = quote_column_names[i]
    with column:
        st.markdown(f"{column_name}")
        st.write(st.session_state.quote_data[selected_symbol][column_name][0])

#graphs
graph_columns = st.columns(2)
with graph_columns[0]:
    df = st.session_state.sentiment_data[selected_symbol]
    fig, ax = plt.subplots()
    ax.plot(df['sentiment_date'], df['daily_sentiment_score'], label='Sentiment Score', marker='o')
    ax.plot(df['sentiment_date'], df['price_change'], label='Normalised Stock Movement', marker='o')

    ax.set_xlabel('Date')
    ax.set_ylabel('Value')
    ax.set_title(f"{selected_symbol} - Sentiment vs. Stock Movement")
    ax.legend()

    st.pyplot(fig)
with graph_columns[1]:
    df = st.session_state.historic_data[selected_symbol]
    fig, ax = plt.subplots()
    ax.plot(df['price_date'], df['price'], label='Close Price', marker='o')

    ax.set_xlabel('Date')
    ax.set_ylabel('Value')
    ax.set_title(f"{selected_symbol} - Historic Close Price 1Y")
    ax.legend()
    fig.autofmt_xdate()
    st.pyplot(fig)

#live crypto price data
while True:
    with placeholder.container():
        figs = st.columns(len(STREAM_SYMBOLS))
        for i, fig in enumerate(figs):
            with fig:
                symbol_name = st.session_state.data[STREAM_SYMBOLS[i]]["description"][0]
                st.markdown(f"{symbol_name}")
                val_col, comparison_col = st.columns(2)
                df = load_live_data(STREAM_SYMBOLS[i])
                value = df["price"][0]
                with val_col:
                    st.write(value)
                with comparison_col:
                    original = st.session_state.data[STREAM_SYMBOLS[i]]["price"][0]
                    st.write(styled_number(value - original), unsafe_allow_html=True)

    time.sleep(1)
