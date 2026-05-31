import yfinance as yf

import pandas as pd

# ==================================================

INTERVAL_MAP = {

    "15m": "15m",

    "1h": "60m",

    "4h": "60m",

    "1d": "1d"
}

# ==================================================

def convert_symbol(symbol):

    if "BTC" in symbol:

        return "BTC-USD"

    if "ETH" in symbol:

        return "ETH-USD"

    if "SOL" in symbol:

        return "SOL-USD"

    if "DOGE" in symbol:

        return "DOGE-USD"

    if "XRP" in symbol:

        return "XRP-USD"

    return "BTC-USD"

# ==================================================

def get_klines(

    symbol,

    interval="15m",

    limit=200
):

    try:

        yf_symbol = convert_symbol(symbol)

        yf_interval = INTERVAL_MAP.get(

            interval,

            "15m"
        )

        df = yf.download(

            yf_symbol,

            interval=yf_interval,

            period="60d",

            progress=False
        )

        if df.empty:

            return pd.DataFrame()

        df = df.reset_index()

        # ==================================================
        # 统一字段
        # ==================================================

        df.columns = [

            "timestamp",

            "open",

            "high",

            "low",

            "close",

            "adj_close",

            "volume"
        ]

        df = df[[

            "timestamp",

            "open",

            "high",

            "low",

            "close",

            "volume"
        ]]

        return df.tail(limit)

    except Exception as e:

        print(f"{symbol} 获取失败: {e}")

        return pd.DataFrame()