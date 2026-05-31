import pandas as pd

df = pd.read_csv("trade_attribution.csv")

golden = df[
    (
        (df["TrendAgent"] == "LONG")
        &
        (df["bos_signal"] == "BULLISH")
    )
    |
    (
        (df["TrendAgent"] == "SHORT")
        &
        (df["bos_signal"] == "BEARISH")
    )
]

risky = df[
    (
        (df["TrendAgent"] == "LONG")
        &
        (df["bos_signal"] == "BEARISH")
    )
    |
    (
        (df["TrendAgent"] == "SHORT")
        &
        (df["bos_signal"] == "BULLISH")
    )
]

def stats(name, data):

    wins = data[data["profit"] > 0]

    losses = data[data["profit"] <= 0]

    gross_profit = wins["profit"].sum()

    gross_loss = abs(losses["profit"].sum())

    pf = (
        gross_profit / gross_loss
        if gross_loss > 0
        else 999
    )

    print("\n====================")
    print(name)
    print("====================")

    print("Trades:", len(data))

    print("Net Profit:",
          round(data["profit"].sum(),2))

    print("Win Rate:",
          round(
              len(wins) /
              len(data) *
              100,
              2
          ))

    print("PF:",
          round(pf,2))

stats("GOLDEN", golden)

stats("RISKY", risky)