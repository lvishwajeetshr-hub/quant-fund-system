import sqlite3
import pandas as pd
import numpy as np

def run_risk_report(db_name="portfolio.db", risk_free_rate=0.07):
    conn = sqlite3.connect(db_name)
    query = "SELECT scheme_name, nav_date, nav FROM daily_nav"
    df = pd.read_sql_query(query, conn)
    conn.close()

    df['nav_date'] = pd.to_datetime(df['nav_date'], format='%d-%m-%Y')
    pivot_df = df.pivot(index='nav_date', columns='scheme_name', values='nav').sort_index()
    
    daily_returns = pivot_df.pct_change().dropna()
    annual_returns = daily_returns.mean() * 250
    annual_volatility = daily_returns.std() * np.sqrt(250)
    sharpe_ratio = (annual_returns - risk_free_rate) / annual_volatility
    correlation_matrix = daily_returns.corr()

    print("\n=== QUARTERLY RISK & PERFORMANCE REPORT ===")
    for fund in pivot_df.columns:
        print(f"Fund: {fund}")
        print(f"  Sharpe Ratio:  {sharpe_ratio[fund]:.2f} (Target > 1.0)")
        print(f"  Volatility:    {annual_volatility[fund]:.2%}\n")
        
    print("=== DIVERSIFICATION CORRELATION ===")
    print(correlation_matrix.to_string(float_format=lambda x: f"{x:.2f}"))

if __name__ == "__main__":
    run_risk_report()