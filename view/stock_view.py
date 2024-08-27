import streamlit as st
from model.ticker_search_service import TickerSearchService
import pandas as pd

class StockView:
    """
    The View component for displaying stock data and analysis results.

    Responsibilities:
        - Display the DCA results and related graphs.
        - Provide input fields for user interaction.
    """

    def __init__(self):
        st.title("Stock DCA Performance")

    def display_dca_results(self, dca_results: pd.DataFrame):
        """
        Displays the DCA results including a line chart for portfolio value over time.

        Args:
            dca_results (pd.DataFrame): The DataFrame containing DCA results to be displayed.
        """
        st.subheader("DCA Portfolio Value Over Time")
        st.line_chart(dca_results['Portfolio Value'])

    def get_user_inputs(self):
        """
        Gets user inputs for the stock analysis.

        Returns:
            tuple: Ticker symbol, investment amount, start date, investment frequency, and custom interval.
        """
        # Company name input with search capability
        company_name = st.text_input("Enter company name:")

        ticker = None
        if company_name:
            # Search for tickers matching the company name
            results = TickerSearchService.search_ticker(company_name)
            if results:
                # Let the user select the correct ticker
                selected = st.selectbox("Select the correct ticker:", results, format_func=lambda x: f"{x[1]} ({x[0]})")
                ticker = selected[0]
            else:
                st.warning("No matching companies found.")

        investment = st.number_input("Investment amount per interval ($):", min_value=1.0, value=100.0)
        start_date = st.date_input("Start date for DCA calculation:", value=pd.Timestamp("2010-01-03"))
        frequency = st.selectbox("Investment frequency:", ["daily", "weekly", "monthly"])

        # Display the custom interval input only if 'daily' is selected
        custom_interval = None
        if frequency == "daily":
            custom_interval = st.number_input("Custom interval (days):", min_value=1, value=1)

        return ticker, investment, start_date, frequency, custom_interval

    def display_additional_metrics(self, total_investment, current_portfolio_value, percentage_increase):
        """
        Display the total investment, current portfolio value, and percentage increase with thousand separators.
        """
        st.write(f"**Total Investment:** ${total_investment:,.2f}")
        st.write(f"**Current Portfolio Value:** ${current_portfolio_value:,.2f}")
        st.write(f"**Percentage Increase:** {percentage_increase:.2f}%")