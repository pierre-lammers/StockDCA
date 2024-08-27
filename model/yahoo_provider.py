import yfinance as yf
from .stock import Stock
from typing import Dict


class YahooProvider:
    """
    Provides a connection to Yahoo Finance and manages the retrieval of stock data.

    Attributes:
        cache (Dict[str, Stock]): A dictionary caching the Stock objects to avoid redundant API calls.
    """

    def __init__(self):
        self.cache: Dict[str, Stock] = {}

    def get_stock(self, ticker: str) -> Stock:
        """
        Retrieves a Stock object for the given ticker, either from the cache or by downloading from Yahoo Finance.

        Args:
            ticker (str): The stock ticker symbol (e.g., 'AAPL').

        Returns:
            Stock: A Stock object containing the ticker and its historical daily price data.
        """
        if ticker in self.cache:
            return self.cache[ticker]

        # Download historical data
        data = yf.download(ticker, start="2000-01-03")
        stock = Stock(ticker=ticker, data=data)

        # Cache the Stock object
        self.cache[ticker] = stock
        return stock

    def clear_cache(self):
        """
        Clears the cache of stored Stock objects.
        """
        self.cache.clear()
