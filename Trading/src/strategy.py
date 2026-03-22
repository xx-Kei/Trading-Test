import pandas as pd

def moving_average_strategy(df, short: int, long: int):
    df = df.copy()
    
    df["MA_short"] = df["Close"].rolling(short).mean()
    df["MA_long"] = df["Close"].rolling(long).mean()

    df["Signal"] = 0
    df.loc[df["MA_short"] > df["MA_long"], "Signal"] = 1
    df.loc[df["MA_short"] < df["MA_long"], "Signal"] = -1

    return df