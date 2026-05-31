import pandas as pd

df = pd.read_csv("trade_attribution.csv")

combo = df[
    df["fvg_signal"] == "BEARISH_FVG"
]

wins = combo[combo["profit"] > 0]
losses = combo[combo["profit"] < 0]

pf = wins["profit"].sum() / abs(losses["profit"].sum())

print()
print("BEARISH FVG ONLY")
print()

print("交易数:", len(combo))
print("净利润:", round(combo["profit"].sum(),2))
print("PF:", round(pf,2))