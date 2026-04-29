import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# --- 1. CONFIG & SETTINGS ---
st.set_page_config(page_title="Quarterly Insights Pro", layout="wide")

def format_to_billions(df):
    """Safely converts numeric financial data to Billions scale."""
    if df is None or df.empty:
        return df
    df_copy = df.copy()
    numeric_cols = df_copy.select_dtypes(include=['number']).columns
    df_copy[numeric_cols] = df_copy[numeric_cols] / 1_000_000_000
    return df_copy.round(3)

# --- 2. USER INPUT ---
st.title("📊 Smart Quarterly Financial Report")
ticker = st.sidebar.text_input("Enter Stock Ticker:", value="TSLA").upper()

if ticker:
    try: # Start of the try block
        with st.spinner(f'Fetching data for {ticker}...'):
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # --- 3. TOP LEVEL METRICS ---
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Current Price", f"${info.get('currentPrice', 'N/A')}")
            col2.metric("Forward P/E", info.get('forwardPE', 'N/A'))
            
            try:
                equity = stock.quarterly_balance_sheet.loc['Stockholders Equity'].iloc[0]
                net_income = stock.quarterly_income_stmt.loc['Net Income'].iloc[0]
                roe = (net_income / equity) * 100
                col3.metric("Quarterly ROE%", f"{roe:.2f}%")
            except:
                col3.metric("Quarterly ROE%", "N/A")
                
            col4.metric("Market Cap", f"${info.get('marketCap', 0) / 1e9:.2f}B")

            # --- 4. TABS SETUP ---
            tab1, tab2, tab3, tab4 = st.tabs(["Income", "Balance Sheet", "Cash Flow", "Charts"])

            with tab1:
                st.subheader("Quarterly Income Statement ($ Billions)")
                st.dataframe(format_to_billions(stock.quarterly_income_stmt), use_container_width=True)

            with tab2:
                st.subheader("Quarterly Balance Sheet ($ Billions)")
                st.dataframe(format_to_billions(stock.quarterly_balance_sheet), use_container_width=True)

            with tab3:
                st.subheader("Quarterly Cash Flow ($ Billions)")
                st.dataframe(format_to_billions(stock.quarterly_cashflow), use_container_width=True)
                
            with tab4:
                st.subheader("1-Year Price Performance")
                hist = stock.history(period="1y")
                fig = go.Figure(data=[go.Candlestick(x=hist.index,
                                open=hist['Open'], high=hist['High'],
                                low=hist['Low'], close=hist['Close'])])
                st.plotly_chart(fig, use_container_width=True)

    except Exception as e: # This MUST follow the try block
        st.error(f"Error loading data for {ticker}. Please ensure the ticker is correct.")
        st.write(e) # This helps you see the actual error if it's not just a bad ticker
        