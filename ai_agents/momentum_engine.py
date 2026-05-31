class MomentumEngine:
    def __init__(self):
        pass

    def detect(self, df):
        close = df["close"]
        volume = df["volume"]

        ema20 = close.ewm(span=20, adjust=False).mean()
        ema50 = close.ewm(span=50, adjust=False).mean()

        # 斜率阈值从0.01降到0.002
        slope = (ema20.iloc[-1] - ema20.iloc[-5]) / ema20.iloc[-5] if len(ema20)>=5 else 0

        avg_volume = volume.rolling(20).mean()
        volume_ratio = volume.iloc[-1] / avg_volume.iloc[-1] if avg_volume.iloc[-1] != 0 else 1

        # 条件放宽：斜率>0.002且成交量倍数>1.5
        if slope > 0.002 and volume_ratio > 1.5:
            return {
                "burst": True,
                "strength": volume_ratio
            }
        return {
            "burst": False,
            "strength": 0
        }