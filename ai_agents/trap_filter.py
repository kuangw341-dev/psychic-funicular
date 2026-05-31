class TrapFilter:
    def __init__(self):
        pass

    # ==================================================
    def check(
        self,
        df
    ):
        # ==================================================
        # 最新K线
        # ==================================================
        candle = df.iloc[-1]
        open_price = candle["open"]
        close_price = candle["close"]
        high_price = candle["high"]
        low_price = candle["low"]

        # ==================================================
        # K线结构
        # ==================================================
        body = abs(
            close_price - open_price
        )
        upper_wick = high_price - max(
            open_price,
            close_price
        )
        lower_wick = min(
            open_price,
            close_price
        ) - low_price

        # ==================================================
        # 上影线过长
        # 假突破风险
        # ==================================================
        if upper_wick > body * 2.5:
            print("""

❌ TrapFilter:

检测到长上影线
禁止交易
""")
            return False

        # ==================================================
        # 下影线过长
        # ==================================================
        if lower_wick > body * 2.5:
            print("""

❌ TrapFilter:

检测到长下影线
禁止交易
""")
            return False

        # ==================================================
        # 波动过小
        # ==================================================
        candle_range = high_price - low_price
        if candle_range <= 0:
            return False

        # ==================================================
        # 极小实体
        # ==================================================
        if body / candle_range < 0.15:
            print("""

❌ TrapFilter:

十字星震荡
禁止交易
""")
            return False

        # ==================================================
        return True