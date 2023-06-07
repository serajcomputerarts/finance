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
timestamps = [price[0] // 1000 for price in prices]  # Adjusted to seconds

# Convert timestamps to datetime objects at 5-minute intervals
dates = [datetime.fromtimestamp(timestamp) for timestamp in timestamps[::5]]

# Extract ETH/USD prices at 5-minute intervals
ethusd_prices = [price[1] for price in prices[::5]]

# Create pandas DataFrame with price data
df = pd.DataFrame({'ETH/USD': ethusd_prices}, index=dates)

# Plot ETH/USD price
plt.plot(df.index, df['ETH/USD'])
plt.xlabel('Time')
plt.ylabel('ETH/USD Price')
plt.title('ETH/USD Price for each 5 minutes')
plt.xticks(rotation=45)
plt.show()
