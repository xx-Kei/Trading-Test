def run_backtest(df, cost = 0.001, slippage = 0.0005):
    df["Return"] = df["Close"].pct_change()

    df["Strategy"] = df["Signal"].shift(1) * df["Return"]
    df["Trade"] = df["Signal"].diff().abs()

    df["Strategy_real"] =df["Strategy"] - df["Trade"] * (cost + slippage)
    df["Cumulative"] = (1 + df["Strategy_real"]).cumprod()

    return df