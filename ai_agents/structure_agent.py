class StructureAgent:

    def __init__(self):

        self.name = "StructureAgent"

    # ==================================================

    def analyze(

        self,

        fast_df,

        slow_df
    ):

        recent_high = (

            fast_df["high"]

            .rolling(20)

            .max()

            .iloc[-1]
        )

        recent_low = (

            fast_df["low"]

            .rolling(20)

            .min()

            .iloc[-1]
        )

        close = fast_df["close"].iloc[-1]

        # ==================================================
        # LONG
        # ==================================================

        if close >= recent_high * 0.995:

            return {

                "signal": "LONG",

                "score": 20,

                "reason": "接近突破高点"
            }

        # ==================================================
        # SHORT
        # ==================================================

        elif close <= recent_low * 1.005:

            return {

                "signal": "SHORT",

                "score": 20,

                "reason": "接近跌破低点"
            }

        # ==================================================

        return {

            "signal": "HOLD",

            "score": 0,

            "reason": "结构中性"
        }