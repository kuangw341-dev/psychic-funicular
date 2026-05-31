class RiskManager:
    def __init__(self):
        # 连续亏损计数器
        self.loss_streak = 0

    def set_loss_streak(self, streak):
        """外部设置连续亏损次数"""
        self.loss_streak = streak

    def reset_loss_streak(self):
        """盈利时重置亏损计数"""
        self.loss_streak = 0

    def calculate(self, confidence, balance, market_regime="SIDEWAYS", trend_strength=0.0):
        # 默认
        leverage = 3
        position_size = 0.05

        if confidence >= 0.35:
            leverage = 5
            position_size = 0.08
        if confidence >= 0.50:
            leverage = 8
            position_size = 0.12
        if confidence >= 0.70:
            leverage = 12
            position_size = 0.18

        # 修正 regime 匹配：支持 "TREND_BULL" 或 "BULL"
        if "BULL" in market_regime or market_regime == "TREND_BULL":
            position_size *= 1.2
        if "BEAR" in market_regime or market_regime == "TREND_BEAR":
            position_size *= 0.8

        if trend_strength > 0.03:
            leverage += 3
            position_size *= 1.5

        # 爆仓风险保护
        liquidation_risk = leverage * position_size
        if liquidation_risk > 2.5:
            leverage *= 0.7
            position_size *= 0.7
            print("\n⚠️ 爆仓风险过高，自动降低杠杆与仓位")

        # 连续亏损保护
        if self.loss_streak >= 3:
            leverage *= 0.5
            position_size *= 0.5
            print("\n⚠️ 连续亏损保护启动")

        # 限制
        if leverage > 20:
            leverage = 20
        if position_size > 0.25:
            position_size = 0.25

        risk_amount = balance * position_size

        return {
            "leverage": round(leverage, 2),
            "position_size": round(position_size, 4),
            "risk_amount": round(risk_amount, 2)
        }