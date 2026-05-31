import pandas as pd

df = pd.read_csv("trade_attribution.csv")

print("\nTOP LOSERS\n")

print(
    df.sort_values(
        "profit"
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