class DivergenceEngine:
    def __init__(self):
        pass

    def detect(self, df):
        if len(df) < 30:
            return {
                "bull_divergence": False,
                "bear_divergence": False
            }

        closes = df["close"]
        volumes = df["volume"]

        # Price
        recent_high = closes.iloc[-1]
        previous_high = closes.iloc[-10]
        recent_low = closes.iloc[-1]
        previous_low = closes.iloc[-10]

        # Volume
        recent_volume = volumes.iloc[-5:].mean()
        old_volume = volumes.iloc[-15:-10].mean()

        # Bear Div
        bear_div = recent_high > previous_high and recent_volume < old_volume

        # Bull Div
        bull_div = recent_low < previous_low and recent_volume < old_volume

        return {
            "bull_divergence": bull_div,
            "bear_divergence": bear_div
        }