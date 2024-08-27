import pandas as pd
from model.stock import Stock
from logger import get_logger
import numpy as np

class StockAnalyzer:
    def __init__(self, stock: Stock):
        self.stock = stock
        self.logger = get_logger(__name__)

    def calculate_dca(self, investment: float, start_date: pd.Timestamp, frequency: str = 'monthly', custom_interval: int = None) -> pd.DataFrame:
        # Retrieve the stock data (assumed to be already sorted by index)
        data = self.stock.data

        self.logger.info(f"Start date: {start_date}")
        self.logger.info(f"Data from start_date: {data.loc[start_date:]}")

        # Check if start_date exists in the data
        if start_date not in data.index:
            nearest_date = data.index[data.index.get_indexer([start_date], method='pad')][0]
            start_date = nearest_date
            self.logger.warning(f"Start date adjusted to the nearest available date before or equal to the given date: {start_date}")

        # Define the interval based on the frequency or custom interval
        if custom_interval:
            step = pd.offsets.BDay(custom_interval)  # Business days only, custom interval
        elif frequency == 'daily':
            step = pd.offsets.BDay(1)  # Business day
        elif frequency == 'weekly':
            step = pd.offsets.Week()  # Every week from start_date
        elif frequency == 'monthly':
            step = pd.offsets.MonthBegin()  # Every month from start_date
        else:
            raise ValueError("Invalid frequency. Choose from 'daily', 'weekly', 'monthly', or provide a custom_interval.")

        # Generate the range of dates based on the interval
        investment_dates = pd.date_range(start=start_date, end=data.index[-1], freq=step)

        # Filter to keep only the dates available in the data (addresses the KeyError)
        investment_dates = investment_dates[investment_dates.isin(data.index)]

        # Vectorized computation of shares purchased and cumulative investment
        prices = data.loc[investment_dates, 'Close']
        shares_purchased = investment / prices
        cumulative_investment = investment * np.arange(1, len(shares_purchased) + 1)
        portfolio_value = shares_purchased.cumsum() * prices

        # Create a DataFrame with the results
        records = pd.DataFrame({
            'Cumulative Investment': cumulative_investment,
            'Shares Purchased': shares_purchased,
            'Portfolio Value': portfolio_value
        }, index=investment_dates)

        return records
