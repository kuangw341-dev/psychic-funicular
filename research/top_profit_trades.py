import pandas as pd

df = pd.read_csv("trade_attribution.csv")

print("\nTOP WINNERS\n")

print(
    df.sort_values(
        "profit",
        ascending=False
    )[
        [
            "profit",
            "TrendAgent",
            "SmartMoneyAgent",
            "bos_signal",
            "choch_signal",
            "fvg_signal",
            "chan_trend",
            "market_regime"
        ]
    ].head(20)
)