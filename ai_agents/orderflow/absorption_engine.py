class AbsorptionEngine:

    def __init__(self):
        pass

    # ==================================================

    def detect(self, df):
        candle = df.iloc[-1]

        body = abs(
            candle["close"] - candle["open"]
        )

        volume = candle["volume"]

        avg_volume = df["volume"].tail(20).mean()

        # ==================================================
        # 吸筹
        # ==================================================

        if (
            volume > avg_volume * 2
            and body < (candle["high"] - candle["low"]) * 0.2
        ):
            return {
                "absorption": True
            }

        # ==================================================

        return {
            "absorption": False
        }