# orderflow/aggressive_flow.py

class AggressiveFlow:

    def __init__(self):
        pass

    # ==================================================

    def detect(self, df):
        candle = df.iloc[-1]
        body = abs(candle["close"] - candle["open"])
        avg_body = abs(df["close"] - df["open"]).tail(20).mean()
        avg_volume = df["volume"].tail(20).mean()

        # ==================================================

        aggressive = (body > avg_body * 2 and candle["volume"] > avg_volume * 2)

        # ==================================================

        return {
            "aggressive_flow": aggressive
        }