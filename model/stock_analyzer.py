from dataclasses import dataclass
import pandas as pd
import numpy as np
from model.stock import Stock
import streamlit as st

@dataclass
class StockAnalyzer:
    
    @staticmethod
    def calculate_dca(stock: Stock, investment: float, start_date: pd.Timestamp, frequency: str = 'monthly', custom_interval: int = None, fee: float = 0.0) -> pd.DataFrame:
        # Retrieve the stock data (assumed to be already sorted by index)
        data = stock.data

        # Check if start_date exists in the data
        if start_date not in data.index:
            nearest_date = data.index[data.index.get_indexer([start_date], method='pad')][0]
            start_date = nearest_date

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
        
        # Adjust the investment amount by subtracting the fee
        adjusted_investment = investment - fee
        if adjusted_investment <= 0:
            raise ValueError("Investment amount after fees must be greater than zero.")
        
        shares_purchased = adjusted_investment / prices
        cumulative_investment = investment * np.arange(1, len(shares_purchased) + 1)
        portfolio_value = shares_purchased.cumsum() * prices

        # Create a DataFrame with the results
        records = pd.DataFrame({
            'Cumulative Investment': cumulative_investment,
            'Shares Purchased': shares_purchased,
            'Portfolio Value': portfolio_value,
            'Fees Paid': fee * np.arange(1, len(shares_purchased) + 1)  # Keep track of total fees paid
        }, index=investment_dates)

        # Return the DCA records and the new row to be added to the portfolio
        return records
