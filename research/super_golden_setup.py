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
    &
    (df["chan_trend"] == "BEAR")
]

print()
print("================================")
print("SUPER GOLDEN SETUP")
print("================================")
print()

print("交易数:", len(gold))

net_profit = gold["profit"].sum()

wins = gold[gold["profit"] > 0]
losses = gold[gold["profit"] < 0]

gross_profit = wins["profit"].sum()
gross_loss = abs(losses["profit"].sum())

pf = gross_profit / gross_loss

print("净利润:", round(net_profit,2))
print("胜率:", round(len(wins)/len(gold)*100,2))
print("PF:", round(pf,2))

print()
print(gold[
    [
        "profit",
        "score",
        "chan_trend"
    ]
])