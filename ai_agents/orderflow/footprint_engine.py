# orderflow/footprint_engine.py

class FootprintEngine:

    def __init__(self):
        pass

    # ==================================================

    def analyze(self, df):
        candle = df.iloc[-1]
        body = abs(candle["close"] - candle["open"])
        range_size = candle["high"] - candle["low"]

        # ==================================================

        imbalance = 0
        if range_size > 0:
            imbalance = body / range_size

        # ==================================================

        return {
            "imbalance": imbalance,
            "strong_move": imbalance > 0.7
        }