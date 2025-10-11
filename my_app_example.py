import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go

st.set_page_config(page_title="Live Updating Charts", layout="wide")
st.title("📈 Live Auto-Updating Raw Value Line Charts (with Smart Scaling)")

# Initialize data
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame({
        "time": [time.time()],
        "A": [100000 + np.random.randn()],
        "B": [100000 + np.random.randn()],
        "C": [100000 + np.random.randn()],
        "D": [100000 + np.random.randn()],
    })

# Layout
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
chart1 = col1.empty()
chart2 = col2.empty()
chart3 = col3.empty()
chart4 = col4.empty()

update_interval = 1
num_points = 30

while True:
    # Append new data
    new_row = {
        "time": time.time(),
        "A": 100000 + np.random.randn() * 50,
        "B": 100000 + np.random.randn() * 50,
        "C": 100000 + np.random.randn() * 50,
        "D": 100000 + np.random.randn() * 50,
    }
    st.session_state.data = pd.concat(
        [st.session_state.data, pd.DataFrame([new_row])],
        ignore_index=True
    ).tail(num_points)

    df = st.session_state.data.copy()
    df["time"] = pd.to_datetime(df["time"], unit="s")

    def make_plot(column):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["time"], y=df[column], mode="lines", name=column))
        fig.update_layout(
            margin=dict(l=10, r=10, t=30, b=10),
            height=250,
            yaxis_title=column,
            template="plotly_white",
        )
        return fig

    # Plot with automatic scaling
    chart1.plotly_chart(make_plot("A"), use_container_width=True)
    chart2.plotly_chart(make_plot("B"), use_container_width=True)
    chart3.plotly_chart(make_plot("C"), use_container_width=True)
    chart4.plotly_chart(make_plot("D"), use_container_width=True)

    time.sleep(update_interval)
