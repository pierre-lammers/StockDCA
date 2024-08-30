from model.stock_analyzer import StockAnalyzer
from model.yahoo_provider import YahooProvider
from view.stock_view import StockView
from logger import get_logger
import pandas as pd

class StockController:
    """
    The Controller component that handles the logic of the application.

    Responsibilities:
        - Interact with the model to fetch stock data.
        - Perform financial analysis using the StockAnalyzer.
        - Update the view with the results.
    """

    def __init__(self):
        self.view = StockView()
        self.provider = YahooProvider()
        self.logger = get_logger(__name__)

    def run(self):
        """
        The main method to run the controller and manage the application flow.
        """

        # Get user inputs from the view
        ticker, investment, start_date, frequency, custom_interval, fee = self.view.get_user_inputs()

        self.logger.info(f"User selected parameters: Ticker={ticker}, Investment=${investment}, Start Date={start_date}, Frequency={frequency}, Custom Interval={custom_interval} days")

        if ticker:
            # Fetch the Stock object using the YahooProvider
            stock = self.provider.get_stock(ticker)

            # Create a StockAnalyzer for the fetched Stock
            analyzer = StockAnalyzer(stock)

            # Calculate DCA based on user input
            dca_results = analyzer.calculate_dca(investment, start_date, frequency, custom_interval, fee)

            # Calculate the total investment, current portfolio value, and percentage increase
            total_investment = dca_results['Cumulative Investment'].iloc[-1]
            current_portfolio_value = dca_results['Portfolio Value'].iloc[-1]
            percentage_increase = ((current_portfolio_value - total_investment) / total_investment) * 100

            # Log the calculated results
            self.logger.info(f"Total Investment: ${total_investment:.2f}")
            self.logger.info(f"Current Portfolio Value: ${current_portfolio_value:.2f}")
            self.logger.info(f"Percentage Increase: {percentage_increase:.2f}%")

            # Display additional metrics
            self.view.display_dca_results_and_metrics(dca_results, total_investment, current_portfolio_value, percentage_increase)

        