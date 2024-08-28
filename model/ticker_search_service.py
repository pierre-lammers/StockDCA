from yahooquery import search
from functools import lru_cache

class TickerSearchService:
    """
    Service class to handle searching for stock tickers based on company names using the yahooquery API.
    """

    @staticmethod
    @lru_cache(maxsize=50)
    def search_ticker(query: str):
        """
        Searches for stock tickers based on the company name using yahooquery.

        Args:
            query (str): The partial or full company name to search for.

        Returns:
            list: A list of tuples containing (ticker, company_name).
        """
        try:
            # Use yahooquery's search function
            result = search(query)
            quotes = result['quotes']
            
            # Filter results to only include stocks and ETFs
            filtered_results = [
                (item['symbol'], item['shortname']) for item in quotes
                if item['quoteType'] in ['EQUITY', 'ETF']
            ]
            return filtered_results
        except Exception as e:
            # Handle exceptions (e.g., when no results are found)
            return []
