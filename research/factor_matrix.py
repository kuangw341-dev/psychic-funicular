import pandas as pd

df = pd.read_csv("trade_attribution.csv")

tests = {

    "Trend+SMC":
    (
        df["TrendAgent_used"] == True
    ) &
    (
        df["SmartMoneyAgent_used"] == True
    ),

    "Trend+Volatility":
    (
        df["TrendAgent_used"] == True
    ) &
    (
        df["VolatilityAgent_used"] == True
    ),

    "SMC+Volatility":
    (
        df["SmartMoneyAgent_used"] == True
    ) &
    (
        df["VolatilityAgent_used"] == True
    ),

    "Trend+Pullback":
    (
        df["TrendAgent_used"] == True
    ) &
    (
        df["PullbackAgent_used"] == True
    ),

    "Trend+SMC+BOS":
    (
        df["TrendAgent_used"] == True
    ) &
    (
        df["SmartMoneyAgent_used"] == True
    ) &
    (
        df["bos_signal"] == "BEARISH"
    ),

    "Trend+SMC+FVG":
    (
        df["TrendAgent_used"] == True
    ) &
    (
        df["SmartMoneyAgent_used"] == True
    ) &
    (
        df["fvg_signal"] == "BEARISH_FVG"
    )
}

print()
print("================================")
print("FACTOR MATRIX")
print("================================")
print()

for name, condition in tests.items():

    sub = df[condition]

    if len(sub) < 2:
        continue

    wins = sub[sub["profit"] > 0]
    losses = sub[sub["profit"] < 0]

    gross_profit = wins["profit"].sum()
    gross_loss = abs(losses["profit"].sum())

    pf = (
        gross_profit / gross_loss
        if gross_loss > 0 else 0
    )

    print(name)
    print("Trades:", len(sub))
    print("Profit:", round(sub["profit"].sum(),2))
    print("PF:", round(pf,2))
    print("--------------------------------")