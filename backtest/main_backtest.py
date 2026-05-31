import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

import pandas as pd

from ai_agents.chief_ai import ChiefAI

# ==================================================
# Trade Attribution 导入
# ==================================================
from analytics.trade_attribution import TradeAttribution

# ==================================================
# Agent Expectancy 导入（新增）
# ==================================================
from analytics.agent_expectancy import AgentExpectancy

# ==================================================
# 加载15m数据
# ==================================================

df_15m = pd.read_csv(
    "data/BTCUSDT_15m.csv"
)

# ==================================================
# 查看列名
# ==================================================

print(df_15m.columns)

# ==================================================
# 自动识别时间列
# ==================================================

time_col = df_15m.columns[0]

# ==================================================
# 转时间
# ==================================================

df_15m[time_col] = pd.to_datetime(
    df_15m[time_col]
)

df_15m.set_index(
    time_col,
    inplace=True
)

# ==================================================
# 自动生成1H
# ==================================================

df_1h = df_15m.resample("1h").agg({
    "open": "first",
    "high": "max",
    "low": "min",
    "close": "last",
    "volume": "sum"
}).dropna()

# ==================================================
# 自动生成4H
# ==================================================

df_4h = df_15m.resample("4h").agg({
    "open": "first",
    "high": "max",
    "low": "min",
    "close": "last",
    "volume": "sum"
}).dropna()

# ==================================================
# 自动生成1D（修改警告）
# ==================================================

df_1d = df_15m.resample("1D").agg({
    "open": "first",
    "high": "max",
    "low": "min",
    "close": "last",
    "volume": "sum"
}).dropna()

# ==================================================
# 重置index
# ==================================================

df_15m.reset_index(inplace=True)
df_1h.reset_index(inplace=True)
df_4h.reset_index(inplace=True)
df_1d.reset_index(inplace=True)

# ==================================================
# 初始化
# ==================================================

chief = ChiefAI()

# ==================================================
# Trade Attribution 实例化
# ==================================================
trade_attribution = TradeAttribution()

from ai_agents.shadow.shadow_manager import ShadowManager

shadow_manager = ShadowManager()

balance = 10000
max_balance = balance
position = None
wins = 0
losses = 0
total_profit = 0
total_loss = 0
total_trades = 0

# ==================================================
# Trade Analytics
# ==================================================

trade_logs = []

# ==================================================
# 新增：交易历史（用于记录决策详情）
# ==================================================
trade_history = []

# ==================================================
# 回测循环
# ==================================================

for i in range(200, len(df_15m)):
    fast_df = df_15m.iloc[:i].copy()
    slow_df = df_1h.iloc[:max(50, i // 4)].copy()
    df4 = df_4h.iloc[:max(50, i // 16)].copy()
    df1d = df_1d.iloc[:max(50, i // 96)].copy()

    current_price = fast_df.iloc[-1]["close"]

    # ==================================================
    # 全局风控
    # ==================================================

    can_trade = chief.global_risk.can_trade(
        balance,
        max_balance
    )

    if not can_trade:
        continue

    # ==================================================
    # AI分析
    # ==================================================

    result = chief.evaluate(
        fast_df,
        slow_df,
        df4,
        df1d,
        balance
    )

    # ==================================================
    # Shadow update
    # ==================================================

    if position is None:
        shadow_manager.update(
            current_price
        )

    # ==================================================
    # 开仓
    # ==================================================

    if position is None:
        if result["action"] != "HOLD":
            leverage = result["leverage"]
            risk_amount = result["risk_amount"]
            qty = (risk_amount * leverage) / current_price

            # 将 reasons 列表转为字符串保存
            reason_str = "; ".join(result["reasons"])

            position = {
                "side": result["action"],
                "entry": current_price,
                "qty": qty,
                "leverage": leverage,
                "tp1_done": False,
                "tp2_done": False,
                "entry_time": fast_df.index[-1],
                "reason": reason_str,
                "market_regime": result["market_regime"],
                "trade_id": f"{i}"   # 使用当前K线索引作为 trade_id
            }

            total_trades += 1

            # ==================================================
            # 开仓成功后记录归因信号（只记录一次）
            # ==================================================
            trade_attribution.record_signal(
                trade_id=position["trade_id"],
                action=result["action"],
                score=result["score"],
                market_regime=result["market_regime"],
                agent_signals=chief.agent_signals,
                bos_signal=result.get("bos_signal"),
                choch_signal=result.get("choch_signal"),
                fvg_signal=result.get("fvg_signal"),
                chan_trend=result.get("chan_trend"),
                divergence=result.get("divergence")
            )

            # ==================================================
            # 新增：记录交易决策详情（开仓时）
            # ==================================================
            decision = result.get("decision_log", {})
            trade_history.append({
                "time": fast_df.index[-1],
                "action": result["action"],
                "bull_score": decision.get("bull_score", 0),
                "bear_score": decision.get("bear_score", 0),
                "gap": decision.get("score_gap", 0),
                "bos": decision.get("bos", None),
                "choch": decision.get("choch", None),
                "sweep": decision.get("sweep", None),
                "regime": decision.get("regime", result["market_regime"]),
                "confidence": result["confidence"],
                "pnl": None,          # 平仓时填充
                "balance": None       # 平仓时填充
            })

            print(f"""

================ OPEN =================

方向:
{position["side"]}

价格:
{round(current_price, 2)}

杠杆:
{leverage}x

仓位:
{round(qty, 4)}

=======================================
""")

    # ==================================================
    # 持仓管理
    # ==================================================

    else:
        entry_price = position["entry"]
        pnl_pct = 0

        # ==================================================
        # LONG
        # ==================================================

        if position["side"] == "LONG":
            pnl_pct = (current_price - entry_price) / entry_price

        # ==================================================
        # SHORT
        # ==================================================

        elif position["side"] == "SHORT":
            pnl_pct = (entry_price - current_price) / entry_price

        # ==================================================
        # EMA趋势强度（保留用于其他判断）
        # ==================================================

        ema20 = fast_df["close"].ewm(
            span=20,
            adjust=False
        ).mean()

        ema50 = fast_df["close"].ewm(
            span=50,
            adjust=False
        ).mean()

        trend_strength = abs(
            ema20.iloc[-1] - ema50.iloc[-1]
        ) / current_price

        # ==================================================
        # 动态SL
        # ==================================================

        stop_loss = 0.01

        # ==================================================
        # 趋势行情开始移动止损
        # ==================================================

        if (

            pnl_pct > 0.03

            and

            (

                result["market_regime"]

                == "TREND_BULL"

                or

                result["market_regime"]

                == "TREND_BEAR"
            )
        ):

            stop_loss = 0.015

        # ==================================================
        # EMA趋势退出
        # ==================================================

        ema20_exit = fast_df["close"].ewm(
            span=20,
            adjust=False
        ).mean()

        ema50_exit = fast_df["close"].ewm(
            span=50,
            adjust=False
        ).mean()

        # ==================================================
        # LONG退出
        # ==================================================

        if position["side"] == "LONG":

            exit_signal = (

                ema20_exit.iloc[-1]

                <

                ema50_exit.iloc[-1]
            )

        # ==================================================
        # SHORT退出
        # ==================================================

        else:

            exit_signal = (

                ema20_exit.iloc[-1]

                >

                ema50_exit.iloc[-1]
            )

        # ==================================================
        # 趋势退出
        # ==================================================

        if exit_signal:

            final_profit = (

                position["qty"]

                * current_price

                * pnl_pct
            )

            balance += final_profit

            if final_profit > 0:
                total_profit += final_profit
                wins += 1
                # ========== 新增：盈利时重置连续亏损计数 ==========
                chief.global_risk.record_win()
            else:
                total_loss += abs(final_profit)
                losses += 1

            # ==================================================
            # Trade Attribution: 记录平仓结果
            # ==================================================
            trade_attribution.record_result(
                position["trade_id"],
                final_profit
            )

            # ==================================================
            # Shadow学习
            # ==================================================

            shadow_manager.create_shadow(

                position["side"],

                entry_price,

                pnl_pct
            )

            chief.shadow_learning.add_record(

                pnl_pct,

                pnl_pct
            )

            # ==================================================
            # 日志
            # ==================================================

            trade_logs.append({

                "side": position["side"],

                "entry_price": entry_price,

                "exit_price": current_price,

                "pnl_pct": pnl_pct,

                "profit": final_profit,

                "result":

                    "WIN"

                    if final_profit > 0

                    else

                    "LOSS",

                "reason": position["reason"],

                "market_regime":

                    position["market_regime"],

                "entry_time":

                    position["entry_time"],

                "exit_time":

                    fast_df.index[-1]
            })

            # ==================================================
            # 新增：更新 trade_history 最后一条记录的 pnl 和 balance
            # ==================================================
            if trade_history:
                trade_history[-1]["pnl"] = final_profit
                trade_history[-1]["balance"] = balance

            print(f'''

🚀 趋势退出

方向:
{position["side"]}

盈利:
{round(final_profit, 2)}

PnL:
{round(pnl_pct * 100, 2)}%

余额:
{round(balance, 2)}

================================
''')

            position = None

        # ==================================================
        # 止损
        # ==================================================

        elif pnl_pct <= -stop_loss:
            loss = abs(
                position["qty"]
                * current_price
                * pnl_pct
            )
            balance -= loss
            total_loss += loss
            losses += 1

            chief.global_risk.record_loss()

            # ==================================================
            # Trade Attribution: 记录平仓结果（亏损为负值）
            # ==================================================
            trade_attribution.record_result(
                position["trade_id"],
                -loss
            )

            # ==================================================
            # Agent学习（兼容 agent_signals 新结构）
            # ==================================================
            for name, data in chief.agent_signals.items():
                # 兼容旧格式（字符串）和新格式（字典）
                if isinstance(data, dict):
                    signal = data.get("signal", None)
                else:
                    signal = data
                if signal == position["side"]:
                    chief.weight_manager.punish(name)
                else:
                    chief.weight_manager.reward(name)

            # ==================================================
            # 记录交易日志
            # ==================================================
            trade_logs.append({
                "side": position["side"],
                "entry_price": entry_price,
                "exit_price": current_price,
                "pnl_pct": pnl_pct,
                "profit": -loss,
                "result": "LOSS",
                "reason": position["reason"],
                "market_regime": position["market_regime"],
                "entry_time": position["entry_time"],
                "exit_time": fast_df.index[-1]
            })

            # ==================================================
            # 新增：更新 trade_history 最后一条记录的 pnl 和 balance
            # ==================================================
            if trade_history:
                trade_history[-1]["pnl"] = -loss
                trade_history[-1]["balance"] = balance

            # ==================================================
            # Shadow Learning
            # ==================================================

            shadow_profit = pnl_pct

            chief.shadow_learning.add_record(

                pnl_pct,

                shadow_profit
            )

            # ==================================================
            # Shadow记录
            # ==================================================

            shadow_manager.create_shadow(

                position["side"],

                entry_price,

                pnl_pct
            )

            print(f"""

❌ 动态止损

亏损:
{round(loss, 2)}

余额:
{round(balance, 2)}

================================
""")

            position = None

    # ==================================================
    # 更新最高余额
    # ==================================================

    if balance > max_balance:
        max_balance = balance

# ==================================================
# Shadow Analysis
# ==================================================

shadow_analysis = chief.shadow_learning.analyze()

print("""

================================
SHADOW LEARNING
================================
""")

print(f"""

平均错失利润:

{round(

    shadow_analysis["avg_missed_profit"] * 100,

    2
)}%
""")

# ==================================================
# 提前止盈
# ==================================================

if shadow_analysis["tp_too_early"]:

    print("""

⚠ AI判断:

当前止盈过早

建议:

让利润奔跑
""")

# ==================================================
# Analytics
# ==================================================

# ==================================================
# Shadow Analytics
# ==================================================

shadow_records = shadow_manager.shadow_positions

shadow_missed = []

# ==================================================

for sp in shadow_records:

    missed = (

        sp["max_profit"]

        - sp["real_profit"]
    )

    shadow_missed.append(missed)

# ==================================================

avg_shadow_missed = 0

if len(shadow_missed) > 0:

    avg_shadow_missed = sum(

        shadow_missed

    ) / len(shadow_missed)

# ==================================================
# 统计
# ==================================================

winrate = 0
if total_trades > 0:
    winrate = (wins / total_trades) * 100

profit_factor = 0
if total_loss > 0:
    profit_factor = total_profit / total_loss

drawdown = (max_balance - balance) / max_balance * 100

# ==================================================
# Analytics
# ==================================================

trades_df = pd.DataFrame(trade_logs)

print("""

================================
TRADE ANALYTICS
================================
""")

# ==================================================
# 多空统计
# ==================================================

long_trades = trades_df[trades_df["side"] == "LONG"]
short_trades = trades_df[trades_df["side"] == "SHORT"]

print(f"""

LONG单数:
{len(long_trades)}

SHORT单数:
{len(short_trades)}
""")

# ==================================================
# 市场环境
# ==================================================

print("""

================================
MARKET REGIME
================================
""")

print(
    trades_df.groupby("market_regime")["profit"].sum()
)

# ==================================================
# 原因分析
# ==================================================

print("""

================================
REASON ANALYSIS
================================
""")

print(
    trades_df.groupby("reason")["profit"].sum()
)

# ==================================================
# 平均盈利
# ==================================================

avg_win = trades_df[trades_df["profit"] > 0]["profit"].mean()
avg_loss = trades_df[trades_df["profit"] < 0]["profit"].mean()

print(f"""

平均盈利:
{round(avg_win, 2) if not pd.isna(avg_win) else 0}

平均亏损:
{round(avg_loss, 2) if not pd.isna(avg_loss) else 0}
""")

# ==================================================
# Shadow Analytics 输出
# ==================================================

print("""

================================
SHADOW ANALYTICS
================================
""")

print(f"""

Shadow记录数:

{len(shadow_records)}

平均错失利润:

{round(

    avg_shadow_missed * 100,

    2
)}%
""")

# ==================================================
# Trade Attribution 报告
# ==================================================
trade_attribution.show_report()
trade_attribution.save_csv()

# ==================================================
# Agent Expectancy 分析（新增）
# ==================================================
expectancy = AgentExpectancy()
expectancy.analyze("trade_attribution.csv")

# ==================================================
# 输出
# ==================================================

print("""

================================
V50 FINAL RESULT
================================
""")

print(f"""

最终余额:
{round(balance, 2)}

总交易:
{total_trades}

胜率:
{round(winrate, 2)}%

Profit Factor:
{round(profit_factor, 2)}

最大回撤:
{round(drawdown, 2)}%

总盈利:
{round(total_profit, 2)}

总亏损:
{round(total_loss, 2)}

================================
""")

# ==================================================
# 新增：保存 trade_history 到 CSV
# ==================================================
if trade_history:
    pd.DataFrame(trade_history).to_csv(
        "trade_log.csv",
        index=False
    )
    print("\n交易日志已保存 trade_log.csv")
else:
    print("\n没有交易记录，trade_log.csv 未生成")