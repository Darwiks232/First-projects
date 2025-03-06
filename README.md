"# First-projects" 
BTC Trading Strategy: Moving Averages vs RSI

Overview

This repository contains a Python script that implements two trading strategies for Bitcoin (BTC-USD) using:

Moving Average (MA) crossovers

Relative Strength Index (RSI)

The goal is to compare the performance of both strategies by calculating cumulative returns.

Features

Fetches 1-hour BTC/USD price data from Yahoo Finance

Calculates 50-period and 100-period moving averages

Implements a trading strategy based on MA crossovers (Golden/Death Cross)

Computes RSI (14-period) and generates buy/sell signals

Simulates trading performance, including transaction costs

Plots cumulative returns for both strategies

Installation

To run this script, install the required Python libraries:

pip install numpy pandas yfinance matplotlib

How It Works

Moving Average Strategy

Buy Signal: When the 50-period MA crosses above the 100-period MA

Sell Signal: When the 50-period MA crosses below the 100-period MA

RSI Strategy

Buy Signal: When RSI falls below 30 (oversold condition)

Sell Signal: When RSI rises above 70 (overbought condition)

Running the Script

Simply execute the Python script:

python trading_strategy.py

The script will download BTC/USD data, compute signals, execute trades, and plot the performance comparison.

Results

At the end of execution, the script prints the difference between the final cumulative returns of both strategies.
