import pandas as pd

df = pd.read_csv("trade_attribution.csv")

combo = df[
    (df["TrendAgent_used"] == True)
    &
    (df["SmartMoneyAgent_used"] == True)
]

print()
print("================================")
print("TREND + SMART MONEY ANALYSIS")
print("================================")
print()

print("交易数:", len(combo))
print("净利润:", round(combo["profit"].sum(), 2))
print("平均利润:", round(combo["profit"].mean(), 2))

wins = combo[combo["profit"] > 0]
losses = combo[combo["profit"] < 0]

print("胜率:", round(len(wins) / len(combo) * 100, 2), "%")

gross_profit = wins["profit"].sum()
gross_loss = abs(losses["profit"].sum())

pf = gross_profit / gross_loss if gross_loss > 0 else 0

print("PF:", round(pf, 2))