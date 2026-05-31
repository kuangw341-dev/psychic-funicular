class DeltaEngine:

    def __init__(self):
        pass

    # ==================================================

    def calculate(self, df):
        buy_delta = 0
        sell_delta = 0

        # ==================================================

        for i in range(len(df)):
            candle = df.iloc[i]

            # ==================================================

            if candle["close"] > candle["open"]:
                buy_delta += candle["volume"]
            else:
                sell_delta += candle["volume"]

        # ==================================================

        return {
            "buy_delta": buy_delta,
            "sell_delta": sell_delta
        }