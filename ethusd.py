import requests
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import mplfinance as mpf

# Fetch historical price data from CoinGecko API
response = requests.get('https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=usd&days=max')
data = response.json()

# Extract price, volume, and timestamp data
prices = data['prices']
volumes = data['total_volumes']
timestamps = [price[0] for price in prices]
prices = [price[1] for price in prices]
volumes = [volume[1] for volume in volumes]

# Convert timestamps to human-readable dates
dates = [datetime.fromtimestamp(timestamp / 1000) for timestamp in timestamps]

# Create pandas dataframe with price and volume data
df = pd.DataFrame({'Close': prices, 'Open': prices, 'High': prices, 'Low': prices, 'Volume': volumes}, index=dates)

# Calculate Ichimoku Cloud indicator values
nine_period_high = df['High'].rolling(window=9).max()
nine_period_low = df['Low'].rolling(window=9).min()
twenty_six_period_high = df['High'].rolling(window=26).max()
twenty_six_period_low = df['Low'].rolling(window=26).min()

df['Tenkan-Sen'] = (nine_period_high + nine_period_low) / 2
df['Kijun-Sen'] = (twenty_six_period_high + twenty_six_period_low) / 2
df['Senkou Span A'] = ((df['Tenkan-Sen'] + df['Kijun-Sen']) / 2).shift(26)
df['Senkou Span B'] = ((df['Close'].rolling(window=52).max() + df['Close'].rolling(window=52).min()) / 2).shift(26)

# Plot price timeline and Ichimoku Cloud
mpf.plot(df, type='candle', style='yahoo', volume=True, ylabel='ETH/USD Price', title='ETH/USD Price with Ichimoku Cloud')
