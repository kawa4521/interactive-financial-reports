import yfinance as yf
import pandas as pd

def get_stock_report(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    
    print(f"\n=== LATEST QUARTERLY REPORT: {ticker_symbol.upper()} ===")
    
    # 1. Financial Statements (Quarterly)
    print("\n[Income Statement - Last 4 Quarters]")
    print(stock.quarterly_income_stmt.iloc[:, :4])
    
    print("\n[Balance Sheet - Last 4 Quarters]")
    print(stock.quarterly_balance_sheet.iloc[:, :4])
    
    print("\n[Cash Flow - Last 4 Quarters]")
    print(stock.quarterly_cashflow.iloc[:, :4])
    
    # 2. Key Metrics (Forward P/E and ROE)
    info = stock.info
    forward_pe = info.get('forwardPE', 'N/A')
    
    # Calculate ROE% (Net Income / Shareholders' Equity)
    try:
        net_income = stock.quarterly_income_stmt.loc['Net Income'].iloc[0]
        total_equity = stock.quarterly_balance_sheet.loc['Stockholders Equity'].iloc[0]
        roe = (net_income / total_equity) * 100
        roe_str = f"{roe:.2f}%"
    except:
        roe_str = "Calculate manually (Data missing in API)"

    print("\n" + "="*40)
    print(f"Forward P/E: {forward_pe}")
    print(f"Quarterly ROE%: {roe_str}")
    print("="*40)

# Example usage:
ticker = input("Enter stock ticker (e.g., AAPL): ")
get_stock_report(ticker)