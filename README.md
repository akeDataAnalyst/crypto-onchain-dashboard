# Bitcoin & Ethereum On-Chain Metrics Dashboard (2024–2026)

[![Live Demo](https://img.shields.io/badge/Streamlit-Live%20Demo-brightgreen)](https://crypto-onchain-dashboard-2pd9pe9zebrbpb6ttdu5qk.streamlit.app/)

Interactive dashboard and Jupyter analysis pipeline tracking Bitcoin and Ethereum market health using price, volume, moving averages, volatility, and correlation metrics.

Focuses especially on:
- The 2025 bull run dynamics
- The early 2026 correction phase (visible in February 2026 data)

## Project Overview

This repository contains a complete end-to-end analysis pipeline:

1. Data collection from public sources (Binance via CCXT, Blockchain.com charts)
2. Cleaning, merging, and feature engineering
3. Calculation of key market health indicators
4. Interactive visualization & interpretation
5. Deployable Streamlit dashboard

Main goal: Demonstrate structured crypto market monitoring skills — price & volume trend analysis, signal detection (MA crossovers, volatility spikes, correlation behavior, liquidity drying), and narrative building from data.

## Key Features

- Daily BTC & ETH price + trading volume (2024 → Feb 2026)
- 7-day and 30-day moving averages
- 30-day annualized volatility
- 90-day rolling BTC-ETH price correlation
- Volume trends (7-day moving average, log scale)
- Interactive Plotly charts
- Streamlit dashboard with date filtering and data download
- Quantitative insights on the 2025 bull run vs. February 2026 correction

## Key Insights (February 2026 Snapshot)

- Trend: BTC above 30d MA only 49.5% of full period; 2/30 days in last month; 0/10 in last 10 days  
- Drawdown: BTC -29.3%, ETH -41.2% from recent peaks  
- Volatility: 30-day annualized → BTC 79.1%, ETH 99.4%  
- Correlation: Latest 90-day BTC-ETH price correlation 0.989 (very tight)  
- Volume: BTC 7-day avg down -26.7% vs previous 30-day average → declining selling pressure

These signals point to a significant correction phase with exhaustion characteristics (low volume on down days).

## Technologies Used

- Data: CCXT (Binance), Blockchain.com API, CoinGecko (metadata)
- Processing: pandas, numpy
- Visualization: Plotly (interactive), Matplotlib/Seaborn (exploration)
- Dashboard: Streamlit
- Notebooks: Jupyter
