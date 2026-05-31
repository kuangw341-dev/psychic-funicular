class CentralZoneDetector:

    def __init__(self):
        pass

    # ==================================================

    def detect(self, df):
        highs = df["high"]
        lows = df["low"]

        recent_high = highs.tail(20).max()
        recent_low = lows.tail(20).min()

        zone_mid = (recent_high + recent_low) / 2
        zone_range = recent_high - recent_low

        # ==================================================
        # 中枢震荡
        # ==================================================

        if zone_range / zone_mid < 0.03:
            return {
                "is_central": True,
                "high": recent_high,
                "low": recent_low
            }

        return {
            "is_central": False,
            "high": recent_high,
            "low": recent_low
        }