import sqlite3

def init_db(db_name="portfolio.db"):
    # This creates the file if it doesn't exist, and connects to it if it does.
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create a table to store daily price/NAV records
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_nav (
            scheme_code INTEGER,
            scheme_name TEXT,
            nav_date TEXT,
            nav REAL,
            PRIMARY KEY (scheme_code, nav_date)
        )
    """)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database and tables initialized successfully.")