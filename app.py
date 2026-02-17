import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ────────────────────────────────────────────────
# Page Configuration
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="BTC & ETH Market Health Dashboard 2024–2026",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ────────────────────────────────────────────────
# Load Data
# ────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(
            'enriched_btc_eth_metrics_2024_current.csv',
            parse_dates=['date'],
            index_col='date'
        )
        df.index = pd.to_datetime(df.index)
        return df
    except FileNotFoundError:
        st.error("Data file not found. Please make sure 'enriched_btc_eth_metrics_2024_current.csv' exists in the same folder.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

df = load_data()

# ────────────────────────────────────────────────
# Header & Introduction
# ────────────────────────────────────────────────
st.title("Bitcoin & Ethereum Market Health Dashboard")
st.markdown("""
Interactive analysis of BTC and ETH price trends, moving averages, volatility, correlation, and volume  
**Time period:** 2024 – February 2026  
**Focus:** 2025 bull phase vs. early 2026 correction signals
""")

# ────────────────────────────────────────────────
# Sidebar Controls
# ────────────────────────────────────────────────
st.sidebar.header("Dashboard Controls")

date_range = st.sidebar.date_input(
    "Select date range",
    value=(df.index.min().date(), df.index.max().date()),
    min_value=df.index.min().date(),
    max_value=df.index.max().date()
)

# Filter data based on selected range
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = df.loc[start_date:end_date]
else:
    filtered_df = df.copy()

# ────────────────────────────────────────────────
# Main Tabs
# ────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Price & Moving Averages",
    "Volatility",
    "BTC-ETH Correlation",
    "Trading Volume",
    "Data Table & Download"
])

# ────────────────────────────────────────────────
# Tab 1: Price + 30d MA with dual axis
# ────────────────────────────────────────────────
with tab1:
    st.subheader("BTC & ETH Prices with 30-Day Moving Averages")

    fig1 = make_subplots(specs=[[{"secondary_y": True}]])

    # BTC traces
    fig1.add_trace(
        go.Scatter(x=filtered_df.index, y=filtered_df['btc_price_usd'],
                   name='BTC Price', line=dict(color='orange')),
        secondary_y=False
    )
    fig1.add_trace(
        go.Scatter(x=filtered_df.index, y=filtered_df['btc_price_30d_ma'],
                   name='BTC 30d MA', line=dict(color='darkorange', width=3)),
        secondary_y=False
    )

    # ETH traces
    fig1.add_trace(
        go.Scatter(x=filtered_df.index, y=filtered_df['eth_price_usd'],
                   name='ETH Price', line=dict(color='blue')),
        secondary_y=True
    )
    fig1.add_trace(
        go.Scatter(x=filtered_df.index, y=filtered_df['eth_price_30d_ma'],
                   name='ETH 30d MA', line=dict(color='navy', width=3)),
        secondary_y=True
    )

    # Highlight correction period (if in range)
    if pd.to_datetime('2026-02-01') <= filtered_df.index.max() and pd.to_datetime('2026-02-16') >= filtered_df.index.min():
        fig1.add_vrect(
            x0='2026-02-01', x1='2026-02-16',
            fillcolor="red", opacity=0.12, line_width=0,
            annotation_text="Early 2026 Correction",
            annotation_position="top left",
            annotation_font_size=14,
            annotation_font_color="red"
        )

    fig1.update_layout(
        title='BTC & ETH Prices with 30-Day Moving Averages',
        xaxis_title='Date',
        yaxis_title='BTC Price (USD)',
        yaxis2_title='ETH Price (USD)',
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=600
    )

    st.plotly_chart(fig1, use_container_width=True)

# ────────────────────────────────────────────────
# Tab 2: Volatility
# ────────────────────────────────────────────────
with tab2:
    st.subheader("30-Day Annualized Volatility – BTC vs ETH")

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=filtered_df.index, y=filtered_df['btc_vol_30d'],
        name='BTC 30d Vol (Ann.)', line=dict(color='orange')
    ))
    fig2.add_trace(go.Scatter(
        x=filtered_df.index, y=filtered_df['eth_vol_30d'],
        name='ETH 30d Vol (Ann.)', line=dict(color='blue')
    ))

    fig2.update_layout(
        title='30-Day Annualized Volatility',
        xaxis_title='Date',
        yaxis_title='Volatility (%)',
        hovermode='x unified',
        height=550
    )

    st.plotly_chart(fig2, use_container_width=True)

# ────────────────────────────────────────────────
# Tab 3: Correlation
# ────────────────────────────────────────────────
with tab3:
    st.subheader("90-Day Rolling Correlation: BTC vs ETH Prices")

    fig3 = px.line(
        filtered_df,
        x=filtered_df.index,
        y='btc_eth_price_corr_90d',
        title='90-Day Rolling Correlation',
        labels={'btc_eth_price_corr_90d': 'Correlation', 'date': 'Date'}
    )

    fig3.update_traces(line=dict(color='purple', width=3))
    fig3.update_layout(
        yaxis_range=[-1, 1],
        height=550,
        shapes=[dict(
            type='line',
            x0=filtered_df.index.min(),
            x1=filtered_df.index.max(),
            y0=0, y1=0,
            line=dict(color='gray', dash='dash')
        )]
    )

    st.plotly_chart(fig3, use_container_width=True)

# ────────────────────────────────────────────────
# Tab 4: Volume
# ────────────────────────────────────────────────
with tab4:
    st.subheader("7-Day Average Daily Volume (Log Scale)")

    fig4 = go.Figure()

    fig4.add_trace(go.Scatter(
        x=filtered_df.index, y=filtered_df['btc_volume_7d_ma'],
        name='BTC 7d Avg Volume', line=dict(color='orange')
    ))
    fig4.add_trace(go.Scatter(
        x=filtered_df.index, y=filtered_df['eth_volume_7d_ma'],
        name='ETH 7d Avg Volume', line=dict(color='blue')
    ))

    fig4.update_layout(
        title='7-Day Average Daily Volume (Log Scale)',
        xaxis_title='Date',
        yaxis_title='Volume (log scale)',
        yaxis_type='log',
        hovermode='x unified',
        height=550
    )

    st.plotly_chart(fig4, use_container_width=True)

# ────────────────────────────────────────────────
# Tab 5: Data & Download
# ────────────────────────────────────────────────
with tab5:
    st.subheader("Recent Data Snapshot (Last 15 Days)")

    recent = filtered_df.tail(15)[[
        'btc_price_usd', 'eth_price_usd',
        'btc_price_30d_ma', 'eth_price_30d_ma',
        'btc_vol_30d', 'eth_vol_30d',
        'btc_eth_price_corr_90d',
        'btc_volume_7d_ma', 'eth_volume_7d_ma'
    ]].round(2)

    st.dataframe(recent.style.format({
        'btc_price_usd': '${:,.0f}',
        'eth_price_usd': '${:,.0f}',
        'btc_price_30d_ma': '${:,.0f}',
        'eth_price_30d_ma': '${:,.0f}',
        'btc_vol_30d': '{:.1f}%',
        'eth_vol_30d': '{:.1f}%',
        'btc_eth_price_corr_90d': '{:.3f}'
    }))

    csv = filtered_df.to_csv().encode('utf-8')
    st.download_button(
        label="Download Full Dataset (CSV)",
        data=csv,
        file_name="btc_eth_metrics_2024_2026.csv",
        mime="text/csv"
    )

# ────────────────────────────────────────────────
# Footer
# ────────────────────────────────────────────────
st.markdown("---")
st.caption("Built by Aklilu Abera| Data source: Binance (via ccxt), processed in Jupyter")