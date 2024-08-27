from dataclasses import dataclass
import pandas as pd

@dataclass
class Stock:
    """
    Represents a stock with its historical daily price data.

    Attributes:
        ticker (str): The stock ticker symbol (e.g., 'AAPL').
        data (pd.DataFrame): A DataFrame containing historical daily prices for the stock.
    """
    ticker: str
    data: pd.DataFrame

    def get_data(self, start_date: pd.Timestamp, end_date: pd.Timestamp) -> pd.DataFrame:
        """
        Returns a subset of the stock's data between two dates.

        Args:
            start_date (pd.Timestamp): The start date for the data subset.
            end_date (pd.Timestamp): The end date for the data subset.

        Returns:
            pd.DataFrame: A DataFrame containing the stock's data between the specified dates.
        """
        if start_date > end_date:
            raise ValueError("start_date must be before end_date.")
        return self.data.loc[start_date:end_date]
