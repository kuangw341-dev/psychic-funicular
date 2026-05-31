class CHOCHEngine:

    # ==================================================
    # CHOCH
    # ==================================================

    def detect(

        self,

        current_trend,

        bos_signal

    ):

        # 上升趋势后出现Bearish BOS

        if (

            current_trend == "BULL"

            and

            bos_signal == "BEARISH"

        ):

            return "BEARISH_CHOCH"

        # 下降趋势后出现Bullish BOS

        if (

            current_trend == "BEAR"

            and

            bos_signal == "BULLISH"

        ):

            return "BULLISH_CHOCH"

        return None