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

print()
print("================================")
print("GOLDEN SETUP V2")
print("================================")
print()

print("交易数:", len(gold))

net_profit = gold["profit"].sum()

wins = gold[gold["profit"] > 0]
losses = gold[gold["profit"] < 0]

winrate = (
    len(wins) / len(gold) * 100
    if len(gold) > 0 else 0
)

gross_profit = wins["profit"].sum()
gross_loss = abs(losses["profit"].sum())

pf = (
    gross_profit / gross_loss
    if gross_loss > 0 else 0
)

print("净利润:", round(net_profit, 2))
print("胜率:", round(winrate, 2), "%")
print("PF:", round(pf, 2))

print()

print(
    gold[
        [
            "profit",
            "TrendAgent",
            "SmartMoneyAgent",
            "bos_signal",
            "fvg_signal"
        ]
    ]
)