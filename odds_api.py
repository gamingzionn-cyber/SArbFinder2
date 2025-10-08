import os
import requests

API_KEY = os.getenv("ODDS_API_KEY")
BASE_URL = "https://api.the-odds-api.com/v4/sports/soccer/odds"

def get_live_odds(region="eu", markets="h2h"):
    """
    Fetch live odds for soccer (H2H markets) from OddsAPI.
    region can be 'uk', 'us', 'eu', etc.
    markets can be 'h2h', 'spreads', 'totals'
    """
    params = {
        "apiKey": API_KEY,
        "regions": region,
        "markets": markets,
        "oddsFormat": "decimal"
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()

    # Flatten data into a standardized list for arbitrage.py
    odds_list = []
    for event in data:
        event_id = event["id"]
        home_team = event["home_team"]
        away_team = event["away_team"]

        for bookmaker in event["bookmakers"]:
            book_name = bookmaker["title"]
            for market in bookmaker["markets"]:
                if market["key"] == "h2h":
                    outcomes = market["outcomes"]
                    for outcome in outcomes:
                        odds_list.append({
                            "event_id": event_id,
                            "book": book_name,
                            "outcome": outcome["name"],
                            "odds": outcome["price"],
                            "match": f"{home_team} vs {away_team}"
                        })
    return odds_list
