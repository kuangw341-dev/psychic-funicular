class PivotEngine:
    def __init__(self, lookback=5):
        self.lookback = lookback

    def detect_pivots(self, df):
        highs = df["high"].values
        lows = df["low"].values

        pivot_highs = []
        pivot_lows = []

        lb = self.lookback

        for i in range(lb, len(df) - lb):
            current_high = highs[i]
            current_low = lows[i]

            left_highs = highs[i - lb:i]
            right_highs = highs[i + 1:i + lb + 1]

            left_lows = lows[i - lb:i]
            right_lows = lows[i + 1:i + lb + 1]

            # Pivot High
            if (
                current_high > max(left_highs)
                and current_high > max(right_highs)
            ):
                pivot_highs.append({
                    "index": i,
                    "price": current_high
                })

            # Pivot Low
            if (
                current_low < min(left_lows)
                and current_low < min(right_lows)
            ):
                pivot_lows.append({
                    "index": i,
                    "price": current_low
                })

        return {
            "pivot_highs": pivot_highs,
            "pivot_lows": pivot_lows
        }