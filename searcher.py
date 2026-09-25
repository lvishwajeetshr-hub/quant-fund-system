import requests

def search_fund(keyword):
    # Use the API's search endpoint instead of the full list
    url = f"https://api.mfapi.in/mf/search?q={keyword}"
    response = requests.get(url).json()
    
    print(f"\nSearch Results for '{keyword}':")
    print("-" * 60)
    
    if not response:
        print("No funds found. Try a shorter keyword.")
        return

    # Filter and display the results
    for fund in response:
        name = fund['schemeName']
        # We only want 'Direct' and 'Growth' plans, ignoring dividends
        if "Direct" in name and "Growth" in name and "IDCW" not in name and "Dividend" not in name:
            print(f"Code: {fund['schemeCode']} | Name: {name}")

if __name__ == "__main__":
    # Example: Searching for a specific Parag Parikh fund
    search_fund("Parag Parikh Flexi")