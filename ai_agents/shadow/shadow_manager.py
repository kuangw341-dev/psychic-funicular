class ShadowManager:

    def __init__(self):
        self.shadow_positions = []

    # ==================================================

    def create_shadow(self, side, entry, real_profit):
        self.shadow_positions.append({
            "side": side,
            "entry": entry,
            "real_profit": real_profit,
            "max_profit": real_profit
        })

    # ==================================================

    def update(self, current_price):
        for sp in self.shadow_positions:
            pnl = 0

            if sp["side"] == "LONG":
                pnl = (current_price - sp["entry"]) / sp["entry"]
            else:
                pnl = (sp["entry"] - current_price) / sp["entry"]

            if pnl > sp["max_profit"]:
                sp["max_profit"] = pnl

            # ==================================================
            # AI学习：
            # 趋势利润是否过早结束
            # ==================================================

            if sp["max_profit"] > sp["real_profit"] * 2:
                sp["hold_too_short"] = True
            else:
                sp["hold_too_short"] = False