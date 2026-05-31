import pandas as pd

df = pd.read_csv("trade_attribution.csv")

golden = df[
    (df["TrendAgent_used"] == True) &
    (df["SmartMoneyAgent_used"] == True) &
    (df["bos_signal"] == "BEARISH") &
    (df["fvg_signal"] == "BEARISH_FVG")
]

print("\n")
print("================================")
print("GOLDEN SETUP DETAIL")
print("================================")
print("\n")

print(golden[
    [
        "profit",
        "TrendAgent",
        "SmartMoneyAgent",
        "bos_signal",
        "fvg_signal",
        "market_regime"
    ]
])