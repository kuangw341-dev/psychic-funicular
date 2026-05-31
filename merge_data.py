import os
import pandas as pd

PAIR = "BTC"
data_dir = f"data/{PAIR}"

csv_files = sorted([f for f in os.listdir(data_dir) if f.endswith(".csv") and "_FULL" not in f])
print(f"发现 {len(csv_files)} 个文件")

if len(csv_files) == 0:
    raise Exception("未发现CSV文件")

STANDARD_COLUMNS = [
    "open_time", "open", "high", "low", "close", "volume",
    "close_time", "quote_asset_volume", "number_of_trades",
    "taker_buy_base", "taker_buy_quote", "ignore"
]

def try_parse(file_path):
    # 尝试无表头模式
    try:
        df = pd.read_csv(file_path, header=None)
        if len(df.columns) == 12:
            df.columns = STANDARD_COLUMNS
            return df, "no_header"
    except:
        pass
    # 尝试有表头模式（第一行作为列名）
    try:
        df = pd.read_csv(file_path)
        # 检查是否包含标准列名
        if set(df.columns).intersection({"open_time", "timestamp", "open"}):
            # 重命名列（若需要）
            return df, "has_header"
    except:
        pass
    return None, None

dfs = []
for file in csv_files:
    path = os.path.join(data_dir, file)
    df, mode = try_parse(path)
    if df is None:
        print(f"跳过 {file}: 无法解析")
        continue

    # 确保 open_time 存在且为数值
    if "open_time" not in df.columns:
        # 尝试其他常见列名
        for col in ["timestamp", "time", "start_time"]:
            if col in df.columns:
                df.rename(columns={col: "open_time"}, inplace=True)
                break
        else:
            print(f"跳过 {file}: 找不到时间列")
            continue

    df["open_time"] = pd.to_numeric(df["open_time"], errors="coerce")
    df = df.dropna(subset=["open_time"])
    # 时间范围过滤（2020-2028）
    df = df[(df["open_time"] >= 1577836800000) & (df["open_time"] <= 1861920000000)]
    if len(df) == 0:
        print(f"跳过 {file}: 时间过滤后无数据")
        continue

    # 确保数值列存在并转换
    for col in ["open", "high", "low", "close", "volume"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        else:
            print(f"跳过 {file}: 缺少列 {col}")
            break
    else:
        df = df.dropna(subset=["open", "high", "low", "close", "volume"])
        df = df[df["high"] >= df["low"]]
        df = df[df["volume"] >= 0]
        df = df[df["close"].diff().fillna(1) != 0]
        dfs.append(df)
        min_t = pd.to_datetime(df["open_time"].min(), unit="ms")
        max_t = pd.to_datetime(df["open_time"].max(), unit="ms")
        print(f"成功: {file} -> {len(df)} 行 ({min_t.date()} ~ {max_t.date()})")

if not dfs:
    raise Exception("没有读取到任何有效数据")

df = pd.concat(dfs, ignore_index=True)
df = df.sort_values("open_time")
df = df.drop_duplicates(subset=["open_time"], keep="last")

print(f"\n最终数据: {len(df)} 行")
print(f"时间范围: {pd.to_datetime(df['open_time'].min(), unit='ms')} 至 {pd.to_datetime(df['open_time'].max(), unit='ms')}")

output_path = os.path.join(data_dir, f"{PAIR}USDT_15m_FULL.csv")
df.to_csv(output_path, index=False)
print(f"已保存至 {output_path}")