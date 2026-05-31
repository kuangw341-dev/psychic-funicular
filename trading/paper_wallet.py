balance = 1000

positions = {}

trade_history = []

# ==================================================

def get_balance():

    global balance

    return round(balance, 2)

# ==================================================

def get_positions():

    global positions

    return positions

# ==================================================

def open_position(

    symbol,

    side,

    price,

    qty
):

    global positions

    positions[symbol] = {

        "side": side,

        "entry_price": price,

        "qty": qty
    }

    print(f"""

🚀 开仓

币种:
{symbol}

方向:
{side}

价格:
{round(price, 4)}

数量:
{round(qty, 4)}
""")

# ==================================================

def close_position(

    symbol,

    price
):

    global balance

    global positions

    global trade_history

    if symbol not in positions:

        return

    pos = positions[symbol]

    side = pos["side"]

    entry = pos["entry_price"]

    qty = pos["qty"]

    pnl = 0

    # ==================================================
    # LONG
    # ==================================================

    if side == "LONG":

        pnl = (

            price - entry
        ) * qty

    # ==================================================
    # SHORT
    # ==================================================

    elif side == "SHORT":

        pnl = (

            entry - price
        ) * qty

    # ==================================================

    balance += pnl

    trade_history.append({

        "symbol": symbol,

        "side": side,

        "pnl": pnl
    })

    print(f"""

✅ 平仓

币种:
{symbol}

方向:
{side}

收益:
{round(pnl, 2)}

余额:
{round(balance, 2)}
""")

    del positions[symbol]