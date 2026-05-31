import pandas as pd

df = pd.read_csv("trade_attribution.csv")

bull = df[
    (df["TrendAgent_used"] == True)
    &
    (df["SmartMoneyAgent_used"] == True)
    &
    (df["bos_signal"] == "BULLISH")
    &
    (df["fvg_signal"] == "BULLISH_FVG")
]

print()
print("================================")
print("BULL GOLDEN SETUP")
print("================================")
print()

print("交易数:", len(bull))

if len(bull) == 0:
    print("没有符合条件的交易")
    exit()

net_profit = bull["profit"].sum()

wins = bull[bull["profit"] > 0]
losses = bull[bull["profit"] < 0]

winrate = len(wins) / len(bull) * 100

gross_profit = wins["profit"].sum()
gross_loss = abs(losses["profit"].sum())

pf = (
    gross_profit / gross_loss
    if gross_loss > 0 else 0
)

avg_win = (
    wins["profit"].mean()
    if len(wins) > 0 else 0
)

avg_loss = (
    losses["profit"].mean()
    if len(losses) > 0 else 0
)

print("净利润:", round(net_profit, 2))
print("胜率:", round(winrate, 2), "%")
print("PF:", round(pf, 2))
print("平均盈利:", round(avg_win, 2))
print("平均亏损:", round(avg_loss, 2))

print()
print("================================")
print("DETAIL")
print("================================")
print()

print(
    bull[
        [
            "profit",
            "TrendAgent",
            "SmartMoneyAgent",
            "bos_signal",
            "fvg_signal",
            "market_regime"
        ]
    ]
)