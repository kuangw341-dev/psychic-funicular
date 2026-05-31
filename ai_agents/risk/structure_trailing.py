class StructureTrailing:

    def __init__(self):
        pass

    # ==================================================

    def get_trailing_sl(self, side, pivots):
        if side == "LONG":
            lows = pivots["pivot_lows"]
            if len(lows) > 0:
                return lows[-1]["price"]

        if side == "SHORT":
            highs = pivots["pivot_highs"]
            if len(highs) > 0:
                return highs[-1]["price"]

        return None