import sqlite3
import pandas as pd

def calculate_trades(db_name="portfolio.db", drift_tolerance=0.05):
    conn = sqlite3.connect(db_name)
    query = """
        SELECT scheme_code, scheme_name, nav 
        FROM daily_nav 
        WHERE nav_date = (SELECT MAX(nav_date) FROM daily_nav)
    """
    latest_data = pd.read_sql_query(query, conn)
    conn.close()

    holdings = {
        122639: {"units": 450.5, "target": 0.60},
        125497: {"units": 150.2, "target": 0.40} 
    }

    total_value = 0
    current_status = {}

    for index, row in latest_data.iterrows():
        code = row['scheme_code']
        if code in holdings:
            current_value = holdings[code]["units"] * row['nav']
            total_value += current_value
            current_status[code] = {
                "name": row['scheme_name'],
                "value": current_value,
                "target": holdings[code]["target"]
            }

    print("\n=== WEEKLY TRADE EXECUTION REPORT ===")
    print(f"Total Portfolio Value: ₹{total_value:,.2f}\n")
    
    for code, data in current_status.items():
        actual_weight = data["value"] / total_value
        drift = actual_weight - data["target"]
        
        print(f"Fund: {data['name']} | Drift: {drift:+.2%}")
        
        if abs(drift) > drift_tolerance:
            trade_amount = (total_value * data["target"]) - data["value"]
            if trade_amount > 0:
                print(f"👉 BUY ₹{trade_amount:,.2f}")
            else:
                print(f"👉 SELL ₹{abs(trade_amount):,.2f}")
        else:
            print("👉 HOLD (Within tolerance)")
        print("-" * 40)

if __name__ == "__main__":
    calculate_trades()