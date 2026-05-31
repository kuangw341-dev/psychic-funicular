import pandas as pd

df = pd.read_csv("trade_attribution.csv")

gold = df[
    (df["TrendAgent_used"] == True)
    &
    (df["SmartMoneyAgent_used"] == True)
    &
    (df["bos_signal"] == "BEARISH")
    &
    (df["fvg_signal"] == "BEARISH_FVG")
]

wins = gold[gold["profit"] > 0]
losses = gold[gold["profit"] < 0]

print()

print("GOLDEN SETUP")

print()

print("交易数:", len(gold))

print(
    "胜率:",
    round(len(wins)/len(gold)*100,2),
    "%"
)

print(
    "平均盈利:",
    round(wins["profit"].mean(),2)
)

print(
    "平均亏损:",
    round(losses["profit"].mean(),2)
)

print(
    "最大盈利:",
    round(gold["profit"].max(),2)
)

print(
    "最大亏损:",
    round(gold["profit"].min(),2)
)