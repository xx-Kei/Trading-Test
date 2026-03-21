import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

investment = 500
# Strategy 1
window1 = 5
window2 = 10
# Strategy 2
window3 = 10
window4 = 20
# Strategy 3
window5 = 50
window6 = 200
cost = 0.001


# Download data
df = yf.download("AAPL", start="2020-01-01", end="2023-01-01")[["Close"]]


# Calculate returns and moving averages
df["Return"] = df["Close"].pct_change()
df["MA5_1"] = df["Close"].rolling(window=window1).mean()
df["MA10_1"] = df["Close"].rolling(window=window2).mean()
df["MA10_2"] = df["Close"].rolling(window=window3).mean()
df["MA20_2"] = df["Close"].rolling(window=window4).mean()
df["MA50_3"] = df["Close"].rolling(window=window5).mean()
df["MA200_3"] = df["Close"].rolling(window=window6).mean()


# Generate signals
df["Signal"] = 0
df.loc[df["MA5_1"] > df["MA10_1"], "Signal"] = 1
df["Signal"] = df["Signal"].shift(1)  # apply signal to next day

df["Signal2"] = 0
df.loc[df["MA10_2"] > df["MA20_2"], "Signal2"] = 1
df["Signal2"] = df["Signal2"].shift(1)

df["Signal3"] = 0
df.loc[df["MA50_3"] > df["MA200_3"], "Signal3"] = 1
df["Signal3"] = df["Signal3"].shift(1)

df.dropna(inplace=True)


# Calculate trades and strategy
df["Trade"] = df["Signal"].diff().abs()
df["Strategy"] = df["Signal"] * df["Return"]
df["Cumulative"] = (1 + df["Strategy"] - df["Trade"] * cost).cumprod() * investment

df["Trade2"] = df["Signal2"].diff().abs()
df["Strategy2"] = df["Signal2"] * df["Return"]
df["Cumulative2"] = (1 + df["Strategy2"] - df["Trade2"] * cost).cumprod() * investment

df["Trade3"] = df["Signal3"].diff().abs()
df["Strategy3"] = df["Signal3"] * df["Return"]
df["Cumulative3"] = (1 + df["Strategy3"] - df["Trade3"] * cost).cumprod() * investment

df["Strategy_after_cost"] = df["Strategy"] - df["Trade"] * cost
df["Cumulative_raw"] = (1+df["Strategy"]).cumprod()
df["Cumulative_cost"] = (1+df["Strategy_after_cost"]).cumprod()


# Plot price and moving averages
plt.figure(figsize=(12,5))
plt.plot(df["Close"], label="Price")
plt.plot(df["MA5_1"], label="MA5")
plt.plot(df["MA10_1"], label="MA10")
plt.title("MA5/MA10")
plt.legend()


# Plot price and moving averages for second strategy 
plt.figure(figsize=(12,5))
plt.plot(df["Close"], label="Price")
plt.plot(df["MA10_2"], label="MA10")
plt.plot(df["MA20_2"], label="MA20")
plt.title("MA10/MA20")
plt.legend()


# Plot price and moving averages for third strategy 
plt.figure(figsize=(12,5))
plt.plot(df["Close"], label="Price")
plt.plot(df["MA50_3"], label="MA50")
plt.plot(df["MA200_3"], label="MA200")
plt.title("MA50/MA200")
plt.legend()

# Plot cumulative strategy comparison
plt.figure(figsize=(12,5))
plt.plot(df["Cumulative"], label="MA5/10")
plt.plot(df["Cumulative2"], label="MA10/20")
plt.plot(df["Cumulative3"], label="MA50/200")
plt.title("Comparative Strategies")
plt.legend()


# Plot comparison for strategy 1 with brokerage fees
plt.figure(figsize=(12,5))
plt.plot(df["Cumulative_raw"], label="No Cost")
plt.plot(df["Cumulative_cost"], label="With Cost")
plt.title("MA5/MA10 inclusive brokerage fees")
plt.legend()
plt.show()