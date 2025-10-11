import json
import os
import time
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

CONN = os.getenv("DATABASE_URL")
engine = create_engine(CONN)

with open("settings.json", "r") as s:
    settings = json.load(s)

SYMBOL_LIST = settings["SYMBOL_LIST"]

st.set_page_config(page_title="Stock Dashboard", layout="wide")
st.title("📈 Stock Dashboard")

placeholder = st.empty()

st.cache_data(ttl=1)
def load_data(symbol):
    query = f"""
    SELECT price 
    FROM live_prices
    WHERE symbol = '{symbol}'
    ORDER BY timestamp DESC LIMIT 1
    """
    df = pd.read_sql(query, engine)
    return df

def styled_number(value, size=16):
    color = "green" if value > 0 else "red" if value < 0 else "black"
    sign = "+" if value > 0 else "−" if value < 0 else ""
    return f"<span style='color:{color}; font-size:{size}px;'>{sign}{abs(value):.2f}</span>"

st.session_state.data = []
for symbol in SYMBOL_LIST:
    df = load_data(symbol)
    st.session_state.data.append(df["price"][0])

while True:
    with placeholder.container():
        figs = st.columns(len(SYMBOL_LIST))
        for i, fig in enumerate(figs):
            with fig:
                st.markdown(f"{SYMBOL_LIST[i]}")
                val_col, comparison_col = st.columns(2)
                df = load_data(SYMBOL_LIST[i])
                value = df["price"][0]
                with val_col:
                    st.write(value)
                with comparison_col:
                    original = st.session_state.data[i]
                    st.write(styled_number(value - original), unsafe_allow_html=True)
    time.sleep(1)
