import requests

def search_multiple_funds(keywords):
    for keyword in keywords:
        url = f"https://api.mfapi.in/mf/search?q={keyword}"
        response = requests.get(url).json()
        
        print(f"\n=== Results for '{keyword}' ===")
        
        if not response:
            print("No funds found. Try a shorter keyword.")
            continue # Move to the next keyword in the list

        # Filter and display the results
        for fund in response:
            name = fund['schemeName']
            # We only want 'Direct' and 'Growth' plans
            if "Direct" in name and "Growth" in name and "IDCW" not in name and "Dividend" not in name:
                print(f"Code: {fund['schemeCode']} | Name: {name}")

if __name__ == "__main__":
    # You can add as many fund names to this list as you want
    my_fund_searches = [
        "Parag Parikh Flexi", 
        "HDFC Top 100", 
        "Quant Small Cap",
        "ICICI Nifty 50"
    ]
    
    search_multiple_funds(my_fund_searches)