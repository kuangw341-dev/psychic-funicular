class CentralEngine:
    def __init__(self):
        pass

    def detect_central(self, bis):
        if len(bis) < 3:
            return None

        recent = bis[-3:]

        highs = []
        lows = []

        for b in recent:
            highs.append(max(b["start_price"], b["end_price"]))
            lows.append(min(b["start_price"], b["end_price"]))

        upper = min(highs)
        lower = max(lows)

        if lower < upper:
            return {
                "upper": upper,
                "lower": lower,
                "strength": upper - lower
            }

        return None