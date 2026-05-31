import pandas as pd

df = pd.read_csv("trade_attribution.csv")

sub = df[
    df["VolatilityAgent_used"] == True
]

print()
print("================================")
print("VOLATILITY DEEP DIVE")
print("================================")
print()

print("交易数:", len(sub))
print()

print(
    sub[
        [
            "profit",
            "TrendAgent",
            "SmartMoneyAgent",
            "bos_signal",
            "fvg_signal",
            "market_regime"
        ]
    ]
)

print()
print("总利润:", round(sub["profit"].sum(), 2))

wins = sub[sub["profit"] > 0]
losses = sub[sub["profit"] < 0]

gross_profit = wins["profit"].sum()
gross_loss = abs(losses["profit"].sum())

pf = (
    gross_profit / gross_loss
    if gross_loss > 0 else 0
)

print("PF:", round(pf, 2))