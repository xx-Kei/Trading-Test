def calculate_metrics(df):
    total_return = df["Cumulative"].iloc[-1] - 1
    sharpe = df["Strategy_real"].mean() / df["Strategy_real"].std()
    max_drawdown = (df["Cumulative"].cummax() - df["Cumulative"]).max()

    return {
        "Total Return": total_return,
        "Sharpe Ratio": sharpe,
        "Max Drawdown": max_drawdown
    }