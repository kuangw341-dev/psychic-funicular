import pandas as pd

df = pd.read_csv("trade_attribution.csv")

# 保留没有使用 PullbackAgent 的交易
filtered = df[df["PullbackAgent_used"] != True]

print()
print("原始交易数:", len(df))
print("过滤后交易数:", len(filtered))

print()
print("原始利润:", round(df["profit"].sum(), 2))
print("过滤后利润:", round(filtered["profit"].sum(), 2))