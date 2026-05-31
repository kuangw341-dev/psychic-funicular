import pandas as pd

df = pd.read_csv("trade_attribution.csv")

combo = df[
    (df["TrendAgent_used"] == True)
    &
    (df["SmartMoneyAgent_used"] == True)
    &
    (df["PullbackAgent_used"] == False)
]

print()
print("================================")
print("TREND + SMC (NO PULLBACK)")
print("================================")
print()

print("交易数:", len(combo))

net_profit = combo["profit"].sum()

print("净利润:", round(net_profit, 2))

wins = combo[combo["profit"] > 0]
losses = combo[combo["profit"] < 0]

winrate = len(wins) / len(combo) * 100 if len(combo) > 0 else 0

gross_profit = wins["profit"].sum()
gross_loss = abs(losses["profit"].sum())

pf = gross_profit / gross_loss if gross_loss > 0 else 0

print("胜率:", round(winrate, 2), "%")
print("PF:", round(pf, 2))