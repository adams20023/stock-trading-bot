import alpaca_trade_api as tradeapi
import pandas as pd
from datetime import datetime, timedelta

# Alpaca API credentials
API_KEY = 'PK2YBC1ATKLATOIYJ9Z4'     # Replace with your actual API key
API_SECRET = '764iYcJnb752mR0GlhTN7P7xlooh2cY4h5nJglaA'  # Replace with 
your actual API secret
BASE_URL = 'https://paper-api.alpaca.markets/v2'  # Use the paper trading 
API 
URL for testing

# Initialize the Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# Define the stock to trade
stock = 'AAPL'

# Get account information
account = api.get_account()
print(f'Account equity: ${account.equity}')

# Define the trading strategy
def trading_strategy():
    # Fetch historical data
    barset = api.get_barset(stock, 'day', limit=5)
    bars = barset[stock]

    # Calculate simple moving averages (SMA)
    closing_prices = [bar.c for bar in bars]
    sma_short = 
pd.Series(closing_prices).rolling(window=3).mean().iloc[-1]
    sma_long = pd.Series(closing_prices).rolling(window=5).mean().iloc[-1]

    print(f'SMA Short: {sma_short}, SMA Long: {sma_long}')

    # Buy signal: short-term SMA crosses above long-term SMA
    if sma_short > sma_long:
        print('Buy signal detected')
        try:
            api.submit_order(
                symbol=stock,
                qty=1,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
            print('Order submitted')
        except Exception as e:
            print(f'Error submitting order: {e}')

    # Sell signal: short-term SMA crosses below long-term SMA
    elif sma_short < sma_long:
        print('Sell signal detected')
        try:
            api.submit_order(
                symbol=stock,
                qty=1,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
            print('Order submitted')
        except Exception as e:
            print(f'Error submitting order: {e}')
    else:
        print('No clear signal')

# Run the trading strategy
trading_strategy()
