import sqlite3
import pandas as pd
import numpy as np

def analyze_portfolio(db_name="portfolio.db", risk_free_rate=0.07):
    # 1. Connect to the Memory (Database)
    conn = sqlite3.connect(db_name)
    
    # 2. Extract the raw NAV data
    query = "SELECT scheme_name, nav_date, nav FROM daily_nav"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # 3. Clean and restructure the data
    # Convert text dates into actual time objects
    df['nav_date'] = pd.to_datetime(df['nav_date'], format='%d-%m-%Y')
    
    # Pivot the table so each column is a fund and each row is a date
    pivot_df = df.pivot(index='nav_date', columns='scheme_name', values='nav')
    pivot_df = pivot_df.sort_index()

    # 4. Calculate Daily Returns (The percentage change day-over-day)
    daily_returns = pivot_df.pct_change().dropna()

    # 5. Calculate Core Risk Metrics
    # Annualized return (assuming 250 trading days in a year)
    annual_returns = daily_returns.mean() * 250
    
    # Annualized volatility (Standard Deviation)
    annual_volatility = daily_returns.std() * np.sqrt(250)
    
    # Sharpe Ratio (Excess return per unit of risk)
    sharpe_ratio = (annual_returns - risk_free_rate) / annual_volatility

    # 6. Calculate Correlation Matrix
    correlation_matrix = daily_returns.corr()

    # 7. Print the Intelligence Report
    print("\n=== FUND PERFORMANCE & RISK REPORT ===")
    for fund in pivot_df.columns:
        print(f"Fund: {fund}")
        print(f"  Annual Return: {annual_returns[fund]:.2%}")
        print(f"  Volatility:    {annual_volatility[fund]:.2%}")
        print(f"  Sharpe Ratio:  {sharpe_ratio[fund]:.2f}\n")
        
    print("=== DIVERSIFICATION (CORRELATION MATRIX) ===")
    print("Note: 1.0 means identical movement. Lower is better for diversification.")
    print(correlation_matrix.to_string(float_format=lambda x: f"{x:.2f}"))

if __name__ == "__main__":
    analyze_portfolio()