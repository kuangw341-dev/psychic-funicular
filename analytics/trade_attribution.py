import pandas as pd
import os


class TradeAttribution:

    def __init__(self):
        self.records = {}

    # ==========================================
    # 开仓记录
    # ==========================================

    def record_signal(
        self,
        trade_id,
        action,
        score,
        market_regime,
        agent_signals,
        bos_signal=None,
        choch_signal=None,
        fvg_signal=None,
        chan_trend=None,
        divergence=None
    ):

        # 提取每个 Agent 的信号字符串（兼容新/旧结构）
        def extract_signal(val):
            if isinstance(val, dict):
                return val.get("signal", None)
            return val

        # 提取 used 标志（兼容新/旧结构）
        def extract_used(val):
            if isinstance(val, dict):
                return val.get("used", False)
            return False

        self.records[trade_id] = {

            "trade_id": trade_id,

            "action": action,

            "score": score,

            "market_regime": market_regime,

            "profit": None,

            # Agent 信号（只存字符串）
            "TrendAgent": extract_signal(agent_signals.get("TrendAgent")),
            "StructureAgent": extract_signal(agent_signals.get("StructureAgent")),
            "SmartMoneyAgent": extract_signal(agent_signals.get("SmartMoneyAgent")),
            "VolatilityAgent": extract_signal(agent_signals.get("VolatilityAgent")),
            "PullbackAgent": extract_signal(agent_signals.get("PullbackAgent")),

            # Agent 是否参与最终决策（新增）
            "TrendAgent_used": extract_used(agent_signals.get("TrendAgent")),
            "StructureAgent_used": extract_used(agent_signals.get("StructureAgent")),
            "SmartMoneyAgent_used": extract_used(agent_signals.get("SmartMoneyAgent")),
            "VolatilityAgent_used": extract_used(agent_signals.get("VolatilityAgent")),
            "PullbackAgent_used": extract_used(agent_signals.get("PullbackAgent")),

            # ICT
            "bos_signal": bos_signal,
            "choch_signal": choch_signal,
            "fvg_signal": (
                fvg_signal["type"]
                if isinstance(fvg_signal, dict)
                else fvg_signal
            ),

            # Chan
            "chan_trend": chan_trend,
            "divergence": divergence
        }

    # ==========================================
    # 平仓记录
    # ==========================================

    def record_result(self, trade_id, profit):
        if trade_id in self.records:
            self.records[trade_id]["profit"] = profit

    # ==========================================
    # 保存CSV
    # ==========================================

    def save_csv(self, path="trade_attribution.csv"):
        if len(self.records) == 0:
            return

        df = pd.DataFrame(list(self.records.values()))
        df.to_csv(path, index=False)

        print(f"""

================================
TRADE ATTRIBUTION SAVED
================================

{path}

Records:
{len(df)}

================================
""")

    # ==========================================
    # Agent统计（基于 used 字段）
    # ==========================================

    def show_agent_report(self):
        if len(self.records) == 0:
            return

        df = pd.DataFrame(list(self.records.values()))
        df = df[df["profit"].notna()]

        print("""

================================
AGENT ATTRIBUTION (USED-BASED)
================================
""")

        agents = [
            "TrendAgent",
            "StructureAgent",
            "SmartMoneyAgent",
            "VolatilityAgent",
            "PullbackAgent"
        ]

        for agent in agents:
            used_col = f"{agent}_used"
            if used_col not in df.columns:
                continue

            # 筛选该 Agent 真正参与的交易
            trades = df[df[used_col] == True]
            if len(trades) == 0:
                continue

            profit = trades[trades["profit"] > 0]["profit"].sum()
            loss = abs(trades[trades["profit"] < 0]["profit"].sum())
            pf = round(profit / loss, 2) if loss > 0 else 999
            total = trades["profit"].sum()

            print(f"""

{agent}

参与次数:
{len(trades)}

净利润:
{round(total, 2)}

盈亏比:
{pf}

--------------------------------
""")

    # ==========================================
    # ICT统计（不变）
    # ==========================================

    def show_ict_report(self):
        if len(self.records) == 0:
            return

        df = pd.DataFrame(list(self.records.values()))
        df = df[df["profit"].notna()]

        print("""

================================
ICT ATTRIBUTION
================================
""")

        for signal in ["bos_signal", "choch_signal", "fvg_signal"]:
            print(f"\n{signal}\n")
            groups = df.groupby(signal)["profit"].sum()
            print(groups)

    # ==========================================
    # 总报告
    # ==========================================

    def show_report(self):
        self.show_agent_report()
        self.show_ict_report()