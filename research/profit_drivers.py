import pandas as pd

df = pd.read_csv("trade_attribution.csv")

# 黄金组合
golden_trades = df[
    ((df["TrendAgent"]=="LONG") & (df["bos_signal"]=="BULLISH")) |
    ((df["TrendAgent"]=="SHORT") & (df["bos_signal"]=="BEARISH"))
]

print("GOLDEN TRADES\n", golden_trades.sort_values("profit", ascending=False).head(20))

# 高亏组合
risky_trades = df[
    ((df["TrendAgent"]=="LONG") & (df["bos_signal"]=="BEARISH")) |
    ((df["TrendAgent"]=="SHORT") & (df["bos_signal"]=="BULLISH"))
]

print("\nRISKY TRADES\n", risky_trades.sort_values("profit").head(20))