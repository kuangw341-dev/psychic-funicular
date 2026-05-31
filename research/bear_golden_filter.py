import pandas as pd

df = pd.read_csv("trade_attribution.csv")

# 黄金组合
gold = df[
    (df["TrendAgent_used"] == True)
    &
    (df["SmartMoneyAgent_used"] == True)
    &
    (df["bos_signal"] == "BEARISH")
    &
    (df["fvg_signal"] == "BEARISH_FVG")
]

print()
print("================================")
print("BEAR GOLDEN FILTER")
print("================================")
print()

print("交易数:", len(gold))
print("净利润:", round(gold["profit"].sum(), 2))

print()
print("================================")
print("SCORE ANALYSIS")
print("================================")
print()

print(
    gold[
        [
            "profit",
            "score"
        ]
    ].sort_values(
        "profit",
        ascending=False
    )
)

print()
print("平均Score:", round(gold["score"].mean(), 2))

print()

# Chan分析
if "chan_trend" in gold.columns:

    print("================================")
    print("CHAN ANALYSIS")
    print("================================")
    print()

    print(
        gold.groupby(
            "chan_trend"
        )["profit"].agg(
            ["count", "sum", "mean"]
        )
    )

    print()

# Divergence分析
if "divergence" in gold.columns:

    print("================================")
    print("DIVERGENCE ANALYSIS")
    print("================================")
    print()

    print(
        gold.groupby(
            "divergence"
        )["profit"].agg(
            ["count", "sum", "mean"]
        )
    )

    print()

# Top Winners
print("================================")
print("TOP WINNERS")
print("================================")
print()

print(
    gold.nlargest(
        5,
        "profit"
    )[
        [
            "profit",
            "score",
            "chan_trend",
            "divergence",
            "market_regime"
        ]
    ]
)

print()

# Top Losers
print("================================")
print("TOP LOSERS")
print("================================")
print()

print(
    gold.nsmallest(
        5,
        "profit"
    )[
        [
            "profit",
            "score",
            "chan_trend",
            "divergence",
            "market_regime"
        ]
    ]
)