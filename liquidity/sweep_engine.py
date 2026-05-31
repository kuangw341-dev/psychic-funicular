class LiquiditySweepEngine:

    # ==================================================
    # Sweep检测
    # ==================================================

    def detect(

        self,

        df,

        lookback=20

    ):

        highs = df["high"]
        lows = df["low"]
        closes = df["close"]

        recent_high = highs.iloc[
            -lookback:-2
        ].max()

        recent_low = lows.iloc[
            -lookback:-2
        ].min()

        current_high = highs.iloc[-1]
        current_low = lows.iloc[-1]

        current_close = closes.iloc[-1]

        # ==================================================
        # 扫高回落
        # ==================================================

        if (

            current_high > recent_high

            and

            current_close < recent_high

        ):

            return "SWEEP_HIGH"

        # ==================================================
        # 扫低反弹
        # ==================================================

        if (

            current_low < recent_low

            and

            current_close > recent_low

        ):

            return "SWEEP_LOW"

        return None