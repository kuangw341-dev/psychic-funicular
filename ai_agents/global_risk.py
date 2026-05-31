class GlobalRiskController:
    def __init__(self):
        self.daily_loss = 0
        self.max_daily_loss = 0.05
        self.max_drawdown = 0.15
        self.cooldown = 0
        self.loss_streak = 0

    def can_trade(self, balance, peak_balance):
        if self.cooldown > 0:
            self.cooldown -= 1
            print("\n⚠️ 系统冷却中")
            return False

        drawdown = (peak_balance - balance) / peak_balance
        if drawdown >= self.max_drawdown:
            print("\n❌ 超过最大回撤限制，停止交易")
            return False

        return True

    def record_win(self):
        self.loss_streak = 0

    def record_loss(self):
        self.loss_streak += 1
        if self.loss_streak >= 5:
            self.cooldown = 20
            print("\n⚠️ 连续亏损熔断，暂停20根K线")