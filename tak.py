import numpy as np 
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Download BTC-USD data from Yahoo Finance
try:
    data = yf.download('BTC-USD', start='2024-01-01', end='2025-01-01', interval='1h')
except Exception as e:
    print(f"Error downloading data: {e}")

# Drop any missing values
data = data.dropna()

# Set global plot parameters for a dark theme
plt.rcParams['axes.facecolor'] = '#2E2E2E'  # Gray background color for axes
plt.rcParams['figure.facecolor'] = '#2E2E2E'  # Gray background color for figure
plt.rcParams['axes.edgecolor'] = 'white'  # Color of the axes edge
plt.rcParams['axes.labelcolor'] = 'white'  # Color of the axes labels
plt.rcParams['xtick.color'] = 'white'  # Color of the x-axis tick labels
plt.rcParams['ytick.color'] = 'white'  # Color of the y-axis tick labels
plt.rcParams['text.color'] = 'white'  # Color of the text
plt.rcParams['legend.facecolor'] = '#2E2E2E'  # Background color of the legend
plt.rcParams['legend.edgecolor'] = 'white'  # Edge color of the legend
plt.rcParams['grid.color'] = 'gray'  # Color of the grid
plt.rcParams['grid.linestyle'] = '--'  # Line style of the grid
plt.rcParams['grid.linewidth'] = 0.5  # Line width of the grid
plt.rcParams['grid.alpha'] = 0.7  # Transparency of the grid

# Plot BTC/USD closing prices
plt.plot(data['Close'])
plt.title('BTC/USD Closing Prices')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.show()

# Rename columns for easier access
data.rename(columns={'Close': 'close', 'High': 'high', 'Low': 'low', 'Open': 'open', 'Volume': 'volume'}, inplace=True)
print(data.head())

# Calculate 50-period and 100-period moving averages
data['MA50'] = data['close'].rolling(50).mean()
data['MA100'] = data['close'].rolling(100).mean()

# Plot closing prices with moving averages for October and November 2024
data[['close', 'MA50', 'MA100']].loc['2024-10-01':'2024-11-30'].plot()
plt.title('BTC/USD Closing Prices with MA50 and MA100 for October and November 2024')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.grid(True)
plt.show()

# Initialize signal column
data['signal'] = np.nan

# Generate buy and sell signals based on moving averages
buy = (data["MA50"] > data["MA100"]) & (data["MA50"].shift(1) < data["MA100"].shift(1))
sell = (data["MA50"] < data["MA100"]) & (data["MA50"].shift(1) > data["MA100"].shift(1))

# Assign signals to the signal column
data.loc[buy, 'signal'] = 1
data.loc[sell, 'signal'] = -1

print(data[data['signal']==1].head())

# Get indices for buy and sell signals in November 2024
idx_open = data.loc[data["signal"] == 1].loc['2024-11-01':'2024-11-30'].index
idx_close = data.loc[data["signal"] == -1].loc['2024-11-01':'2024-11-30'].index

# Plot buy and sell signals on the closing price chart
plt.figure(figsize=(14, 7))
plt.scatter(idx_open, data.loc[idx_open]["close"].loc['2024-11-01':'2024-11-30'] + 1500, color="green", marker="^", label='Buy Signal')
plt.scatter(idx_close, data.loc[idx_close]["close"].loc['2024-11-01':'2024-11-30'] + 1500, color="red", marker="v", label='Sell Signal')
plt.plot(data['close'].loc['2024-11-01':'2024-11-30'], label='Close Price')
plt.plot(data['MA50'].loc['2024-11-01':'2024-11-30'], label='MA50')
plt.plot(data['MA100'].loc['2024-11-01':'2024-11-30'], label='MA100')
plt.title('BTC-USD Buy and Sell Signals for October and November 2024')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.grid(True)
plt.show()

# Function to calculate RSI
def calculate_rsi(data, window):
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Calculate 14-period RSI
data['RSI'] = calculate_rsi(data, 14)
print(data[['close', 'RSI']].tail())

# Generate buy and sell signals based on RSI
rsi_buy = data['RSI'] < 30
rsi_sell = data['RSI'] > 70

# Assign RSI signals to the rsi_signal column
data['rsi_signal'] = np.nan
data.loc[rsi_buy, 'rsi_signal'] = 1
data.loc[rsi_sell, 'rsi_signal'] = -1

# Get indices for RSI buy and sell signals in November 2024
idxrsi_open = data.loc[data["rsi_signal"] == 1].loc['2024-11-01':'2024-11-30'].index
idxrsi_close = data.loc[data["rsi_signal"] == -1].loc['2024-11-01':'2024-11-30'].index

# Plot RSI buy and sell signals on the closing price chart
plt.figure(figsize=(14, 7))
plt.scatter(idxrsi_open, data.loc[idxrsi_open]["close"].loc['2024-11-01':'2024-11-30'] + 2500, color="green", marker="^", label='Buy Signal')
plt.scatter(idxrsi_close, data.loc[idxrsi_close]["close"].loc['2024-11-01':'2024-11-30'] + 2500, color="red", marker="v", label='Sell Signal')
plt.plot(data['close'].loc['2024-11-01':'2024-11-30'], label='Close Price')
plt.title('BTC-USD buy and sell signals with RSI for November 2024')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.grid(True)
plt.show()

# Plot MA buy and sell signals
plt.subplot(2, 1, 1)
plt.scatter(idx_open, data.loc[idx_open]["close"].loc['2024-11-01':'2024-11-30'] + 1500, color="green", marker="^", label='Buy Signal')
plt.scatter(idx_close, data.loc[idx_close]["close"].loc['2024-11-01':'2024-11-30'] + 1500, color="red", marker="v", label='Sell Signal')
plt.plot(data['close'].loc['2024-11-01':'2024-11-30'], label='Close Price')
plt.plot(data['MA50'].loc['2024-11-01':'2024-11-30'], label='MA50')
plt.plot(data['MA100'].loc['2024-11-01':'2024-11-30'], label='MA100')
plt.title('BTC-USD Buy and Sell Signals with MA for October and November 2024')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.grid(True)
plt.legend()

# Plot RSI buy and sell signals
plt.subplot(2, 1, 2)
plt.scatter(idxrsi_open, data.loc[idxrsi_open]["close"].loc['2024-11-01':'2024-11-30'] + 2500, color="blue", marker="^", label='RSI Buy Signal')
plt.scatter(idxrsi_close, data.loc[idxrsi_close]["close"].loc['2024-11-01':'2024-11-30'] + 2500, color="orange", marker="v", label='RSI Sell Signal')
plt.plot(data['close'].loc['2024-11-01':'2024-11-30'], label='Close Price')
plt.title('BTC-USD Buy and Sell Signals with RSI for November 2024')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

# Calculate positions based on MA signals
data["position"] = data["signal"].fillna(method="ffill")

# Define a fixed cost for each transaction
cost_ind = 0.001

# Create a vector of costs
data["cost"] = (np.abs(data["signal"]) * cost_ind).fillna(value=0)

# Compute the percentage change of the asset
data["pct"] = data["close"].pct_change(1)

# Compute the return of the strategy
data["return"] = (data["pct"] * data["position"].shift(1) - data["cost"])*100

# Calculate positions based on RSI signals
data["position_rsi"] = data["rsi_signal"].fillna(method="ffill")

# Create a vector of costs for RSI signals
data["cost_rsi"] = (np.abs(data["rsi_signal"]) * cost_ind).fillna(value=0)

# Compute the return of the RSI strategy
data["return_rsi"] = (data["pct"] * data["position_rsi"].shift(1) - data["cost_rsi"]) * 100

# Plot cumulative returns for MA and RSI strategies
plt.figure(figsize=(14, 14))

# Plot cumulative returns for MA strategy
plt.subplot(2, 1, 1)
data["return"].cumsum().plot(color='purple', title="(ROI) for MA Strategy")
plt.ylabel('Cumulative Return (%)')
plt.xlabel('')
plt.grid(True)

# Plot cumulative returns for RSI strategy
plt.subplot(2, 1, 2)
data["return_rsi"].cumsum().plot(color='orange', title="(ROI) for RSI Strategy")
plt.ylabel('Cumulative Return (%)')
plt.grid(True)
plt.xlabel('')
#Plot both strategies
plt.tight_layout()
plt.show()

#Print the difference between the two strategies
print(data['return'].cumsum()[-1]- data['return_rsi'].cumsum()[-1])
