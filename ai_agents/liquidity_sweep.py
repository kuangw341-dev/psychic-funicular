class LiquiditySweepDetector:

    def __init__(self):
        pass

    # ==================================================

    def detect(self, df, liquidity_data):
        candle = df.iloc[-1]
        close_price = candle["close"]
        high_price = candle["high"]
        low_price = candle["low"]

        equal_highs = liquidity_data["equal_highs"]
        equal_lows = liquidity_data["equal_lows"]

        # ==================================================
        # 扫上方流动性
        # ==================================================

        for level in equal_highs:
            # 插针突破
            if high_price > level:
                # 收回下方
                if close_price < level:
                    return {
                        "sweep_high": True,
                        "sweep_low": False
                    }

        # ==================================================
        # 扫下方流动性
        # ==================================================

        for level in equal_lows:
            if low_price < level:
                if close_price > level:
                    return {
                        "sweep_high": False,
                        "sweep_low": True
                    }

        # ==================================================

        return {
            "sweep_high": False,
            "sweep_low": False
        }