import pandas as pd

df = pd.read_csv("trade_attribution.csv")

combo = df[
    (df["TrendAgent_used"] == True)
    &
    (df["SmartMoneyAgent_used"] == True)
    &
    (df["bos_signal"] == "BEARISH")
]

print()
print("================================")
print("TREND + SMC + BEARISH BOS")
print("================================")
print()

print("交易数:", len(combo))

profit = combo["profit"].sum()

wins = combo[combo["profit"] > 0]
losses = combo[combo["profit"] < 0]

pf = wins["profit"].sum() / abs(losses["profit"].sum())

print("净利润:", round(profit,2))
print("PF:", round(pf,2))