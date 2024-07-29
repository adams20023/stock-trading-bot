import alpaca_trade_api as tradeapi
import pandas as pd

# Alpaca API credentials
API_KEY = 'PKQNCCIJ0A603NQ5KE0I'
API_SECRET = 'OR4i0C0idt064EDNrdoyjVTZYHGoqPvpC21EpxAl'
BASE_URL = 'https://paper-api.alpaca.markets'

# Initialize the Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# Define the stock to trade
stock = 'AAPL'

# Define the trading strategy
def trading_strategy():
    try:
        # Fetch historical data with a custom timeframe
        bars = api.get_bars(
            symbol=stock,
            timeframe=tradeapi.TimeFrame.Hour,  # Use hourly bars
            start='2024-07-01T00:00:00Z',  # Start date in ISO format
            end='2024-07-15T23:59:59Z',    # End date in ISO format
            limit=100,  # Limit the number of bars to 100
            adjustment='raw',  # No adjustments
        ).df  # Get the data as a DataFrame

        # Print the DataFrame to check its structure
        print("DataFrame structure:")
        print(bars.head())  # Print the first few rows of the DataFrame

        # Check if DataFrame is empty
        if bars.empty:
            raise ValueError("DataFrame is empty. Check the symbol or timeframe.")

        # Ensure the 'close' column is present
        if 'close' not in bars.columns:
            print("Available columns:")
            print(bars.columns)
            raise ValueError("Column 'close' not found in DataFrame")

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
                print(f'Error submitting buy order: {e}')

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
                print(f'Error submitting sell order: {e}')
        else:
            print('No clear signal')
    
    except Exception as e:
        print(f'Error executing trading strategy: {e}')

# Run the trading strategy
if __name__ == "__main__":
    trading_strategy()
