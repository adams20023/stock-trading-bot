import alpaca_trade_api as tradeapi
import pandas as pd
from datetime import datetime, timedelta

# Alpaca API credentials
API_KEY = 'PK2YBC1ATKLATOIYJ9Z4'
API_SECRET = '764iYcJnb752mR0GlhTN7P7xlooh2cY4h5nJglaA'
BASE_URL = 'https://paper-api.alpaca.markets'  # Use the paper trading API URL for testing

# Initialize the Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# Define the stock to trade
stock = 'AAPL'

# Get account information
account = api.get_account()
print(f'Account equity: ${account.equity}')

# Define the trading strategy
def trading_strategy():
    try:
        # Fetch historical data
        bars = api.get_bars(
            symbol=stock,
            timeframe='1D',  # Use '1D' for daily bars
            limit=5
        ).df  # Get the data as a DataFrame

        # Calculate simple moving averages (SMA)
        closing_prices = bars['close'].tolist()
        sma_short = pd.Series(closing_prices).rolling(window=3).mean().iloc[-1]
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
    
    except Exception as e:
        print(f'Error executing trading strategy: {e}')

# Run the trading strategy
trading_strategy()

