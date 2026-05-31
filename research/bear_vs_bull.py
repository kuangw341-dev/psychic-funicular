import pandas as pd

df = pd.read_csv("trade_attribution.csv")

bear = df[
    (df["bos_signal"] == "BEARISH")
]

bull = df[
    (df["bos_signal"] == "BULLISH")
]

print()
print("BEAR PROFIT")
print(bear["profit"].sum())

print()
print("BULL PROFIT")
print(bull["profit"].sum())

print()
print("BEAR COUNT")
print(len(bear))

print()
print("BULL COUNT")
print(len(bull))