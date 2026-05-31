class FVGEngine:

    # ==================================================
    # Fair Value Gap
    # ==================================================

    def detect(self, df):

        if len(df) < 5:

            return None

        candle1_high = df["high"].iloc[-3]
        candle1_low = df["low"].iloc[-3]

        candle3_high = df["high"].iloc[-1]
        candle3_low = df["low"].iloc[-1]

        # ==================================================
        # Bullish FVG
        # ==================================================

        if candle3_low > candle1_high:

            return {
                "type": "BULLISH_FVG",
                "gap_low": candle1_high,
                "gap_high": candle3_low
            }

        # ==================================================
        # Bearish FVG
        # ==================================================

        if candle3_high < candle1_low:

            return {
                "type": "BEARISH_FVG",
                "gap_low": candle3_high,
                "gap_high": candle1_low
            }

        return None