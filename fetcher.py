import sqlite3
import requests

def fetch_and_store(scheme_codes, db_name="portfolio.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    for code in scheme_codes:
        # Call the free mfapi.in endpoint
        url = f"https://api.mfapi.in/mf/{code}"
        response = requests.get(url).json()
        
        scheme_name = response.get("meta", {}).get("scheme_name", "Unknown")
        nav_records = response.get("data", [])
        
        # Format the raw JSON data into rows for our database
        batch = [
            (code, scheme_name, item["date"], float(item["nav"]))
            for item in nav_records
        ]
        
        # Insert the rows. 'IGNORE' means if the date already exists, skip it.
        cursor.executemany("""
            INSERT OR IGNORE INTO daily_nav (scheme_code, scheme_name, nav_date, nav)
            VALUES (?, ?, ?, ?)
        """, batch)
        
        print(f"Ingested {len(batch)} records for: {scheme_name}")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Using two real funds for testing: 
    # Parag Parikh Flexi Cap (122639) and HDFC Top 100 (125497)
    test_funds = [122639, 125497]
    fetch_and_store(test_funds)