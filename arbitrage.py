import pandas as pd

def detect_arbitrage(odds_data):
    df = pd.DataFrame(odds_data)
    opportunities = []

    for match in df["match"].unique():
        market = df[df["match"] == match]
        outcomes = market["outcome"].unique()
        if len(outcomes) < 2:
            continue

        best_odds = {}
        for outcome in outcomes:
            best_row = market[market["outcome"] == outcome].sort_values("odds", ascending=False).iloc[0]
            best_odds[outcome] = {
                "book": best_row["book"],
                "odds": best_row["odds"]
            }

        inv_sum = sum(1 / o["odds"] for o in best_odds.values())
        if inv_sum < 1:
            profit_pct = round((1 - inv_sum) * 100, 2)
            opportunities.append({
                "match": match,
                "profit_%": profit_pct,
                "books": best_odds
            })

    return opportunities
