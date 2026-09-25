import sqlite3
import pandas as pd
import numpy as np

def run_risk_report(db_name="portfolio.db", risk_free_rate=0.07):
    conn = sqlite3.connect(db_name)
    query = "SELECT scheme_name, nav_date, nav FROM daily_nav"
    df = pd.read_sql_query(query, conn)
    conn.close()

    df['nav_date'] = pd.to_datetime(df['nav_date'], format='%d-%m-%Y')
    # Pivot sorts the fund names alphabetically as columns
    pivot_df = df.pivot(index='nav_date', columns='scheme_name', values='nav').sort_index()
    
    daily_returns = pivot_df.pct_change().dropna()
    
    # 1. Individual Fund Metrics
    annual_returns = daily_returns.mean() * 250
    annual_volatility = daily_returns.std() * np.sqrt(250)
    sharpe_ratio = (annual_returns - risk_free_rate) / annual_volatility
    correlation_matrix = daily_returns.corr()

    # 2. Portfolio Matrix Math
    # For demonstration, we assign an equal weight to all funds. 
    # If you have 2 funds, this creates array([0.5, 0.5])
    num_assets = len(pivot_df.columns)
    weights = np.repeat(1 / num_assets, num_assets)
    
    # Calculate the Annualized Covariance Matrix
    cov_matrix = daily_returns.cov() * 250
    
    # Calculate overall portfolio return: w^T * R
    port_return = np.dot(weights, annual_returns)
    
    # Calculate overall portfolio volatility: sqrt(w^T * Covariance * w)
    port_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    
    # Calculate combined Sharpe Ratio
    port_sharpe = (port_return - risk_free_rate) / port_volatility

    # 3. Print the Intelligence Report
    print("\n=== OVERALL PORTFOLIO METRICS (Assuming Equal Weights) ===")
    print(f"Expected Annual Return: {port_return:.2%}")
    print(f"Portfolio Risk (Vol):   {port_volatility:.2%}")
    print(f"Portfolio Sharpe Ratio: {port_sharpe:.2f}\n")

    print("=== INDIVIDUAL FUND METRICS ===")
    for fund in pivot_df.columns:
        print(f"Fund: {fund}")
        print(f"  Return: {annual_returns[fund]:.2%} | Risk: {annual_volatility[fund]:.2%} | Sharpe: {sharpe_ratio[fund]:.2f}")
        
    print("\n=== DIVERSIFICATION (CORRELATION MATRIX) ===")
    print(correlation_matrix.to_string(float_format=lambda x: f"{x:.2f}"))

if __name__ == "__main__":
    run_risk_report()