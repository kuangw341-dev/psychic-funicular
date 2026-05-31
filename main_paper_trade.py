import time

from exchange import get_klines

from ai_agents.chief_ai import ChiefAI

from trading.paper_wallet import (

    open_position,

    close_position,

    get_positions,

    get_balance
)

# ==================================================
# 初始化
# ==================================================

chief_ai = ChiefAI()

SYMBOLS = [

    "BTCUSDT",

    "ETHUSDT",

    "SOLUSDT",

    "DOGEUSDT",

    "XRPUSDT"
]

print("""

================================
V50 CORE AI SYSTEM
================================
""")

# ==================================================
# 主循环
# ==================================================

while True:

    try:

        for symbol in SYMBOLS:

            # ==========================================
            # 获取数据
            # ==========================================

            fast_df = get_klines(

                symbol,

                interval="15m",

                limit=200
            )

            slow_df = get_klines(

                symbol,

                interval="1h",

                limit=200
            )

            if fast_df.empty:

                continue

            # ==========================================
            # AI决策
            # ==========================================

            decision = chief_ai.evaluate(

                fast_df,

                slow_df,

                get_balance()
            )

            action = decision["action"]

            confidence = decision["confidence"]

            score = decision["score"]

            leverage = decision["leverage"]

            position_size = decision["position_size"]

            price = float(

                fast_df.iloc[-1]["close"]
            )

            print(f"""

================================

币种:
{symbol}

价格:
{round(price, 4)}

动作:
{action}

评分:
{score}

置信度:
{confidence}

杠杆:
{leverage}

仓位:
{position_size}

余额:
{get_balance()}

================================
""")

            # ==========================================
            # 当前持仓
            # ==========================================

            positions = get_positions()

            # ==========================================
            # 无持仓 -> 开仓
            # ==========================================

            if symbol not in positions:

                if action != "HOLD":

                    risk_amount = (

                        get_balance()

                        * position_size
                    )

                    qty = (

                        risk_amount

                        * leverage
                    ) / price

                    open_position(

                        symbol,

                        action,

                        price,

                        qty
                    )

            # ==========================================
            # 有持仓 -> 平仓
            # ==========================================

            else:

                pos = positions[symbol]

                side = pos["side"]

                entry = pos["entry_price"]

                pnl_pct = 0

                # ======================================
                # LONG
                # ======================================

                if side == "LONG":

                    pnl_pct = (

                        price - entry
                    ) / entry

                # ======================================
                # SHORT
                # ======================================

                elif side == "SHORT":

                    pnl_pct = (

                        entry - price
                    ) / entry

                # ======================================
                # 止盈
                # ======================================

                if pnl_pct >= 0.02:

                    print("✅ 达到止盈")

                    close_position(

                        symbol,

                        price
                    )

                # ======================================
                # 止损
                # ======================================

                elif pnl_pct <= -0.01:

                    print("❌ 达到止损")

                    close_position(

                        symbol,

                        price
                    )

        # ==========================================
        # 等待
        # ==========================================

        time.sleep(30)

    except Exception as e:

        print("主循环错误:", e)

        time.sleep(10)