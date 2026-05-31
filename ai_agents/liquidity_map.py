class LiquidityMap:

    def __init__(self):
        pass

    # ==================================================

    def analyze(self, df):
        highs = df["high"]
        lows = df["low"]

        # ==================================================
        # Equal High
        # ==================================================

        equal_highs = []
        equal_lows = []
        tolerance = 0.0015

        # ==================================================

        for i in range(10, len(df) - 10):
            current_high = highs.iloc[i]
            current_low = lows.iloc[i]

            # ==============================================
            # Equal High
            # ==============================================

            left_high = highs.iloc[i - 5:i]
            right_high = highs.iloc[i + 1:i + 6]

            if (
                abs(left_high.max() - current_high) / current_high < tolerance
                and abs(right_high.max() - current_high) / current_high < tolerance
            ):
                equal_highs.append(current_high)

            # ==============================================
            # Equal Low
            # ==============================================

            left_low = lows.iloc[i - 5:i]
            right_low = lows.iloc[i + 1:i + 6]

            if (
                abs(left_low.min() - current_low) / current_low < tolerance
                and abs(right_low.min() - current_low) / current_low < tolerance
            ):
                equal_lows.append(current_low)

        # ==================================================

        return {
            "equal_highs": equal_highs[-5:],
            "equal_lows": equal_lows[-5:]
        }