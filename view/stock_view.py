import streamlit as st
from model.ticker_search_service import TickerSearchService
from model.yahoo_provider import YahooProvider
from logger import get_logger
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
        self.logger = get_logger(__name__)

        # Define columns as attributes
        self.col1, self.col2 = st.columns([1, 2])

    def display_dca_results(self, dca_results: pd.DataFrame):
        """
        Displays the DCA results including a line chart for portfolio value over time.

        Args:
            dca_results (pd.DataFrame): The DataFrame containing DCA results to be displayed.
        """
        with self.col2:
            st.subheader("DCA Portfolio Value Over Time")
            st.line_chart(dca_results["Portfolio Value"])

    def get_user_inputs(self):
        """
        Gets user inputs for the stock analysis.

        Returns:
            tuple: Ticker symbol, investment amount, start date, investment frequency, and custom interval.
        """
        with self.col1:
            # Company name input with search capability
            company_name = st.text_input("Enter company name:")

            ticker = None
            start_date = None
            if company_name:
                # Search for tickers matching the company name
                results = TickerSearchService.search_ticker(company_name)
                if results:
                    # Let the user select the correct ticker
                    selected = st.selectbox(
                        "Select the correct ticker:",
                        results,
                        format_func=lambda x: f"{x[1]} ({x[0]})",
                    )
                    ticker = selected[0]

                    # Fetch stock data to determine the first available date
                    stock = YahooProvider().get_stock(ticker)
                    first_available_date = stock.data.index.min()
                    self.logger.info(
                        f"Start date of the company {company_name} is {first_available_date}"
                    )
                    start_date = st.date_input(
                        "Start date for DCA calculation:",
                        value=first_available_date,
                        min_value=first_available_date,
                        max_value=pd.Timestamp.today(),
                    )

                else:
                    st.warning("No matching companies found.")

            investment = st.number_input(
                "Investment amount per interval ($):", min_value=1.0, value=100.0
            )
            frequency = st.selectbox(
                "Investment frequency:", ["daily", "weekly", "monthly"]
            )

            # Display the custom interval input only if 'daily' is selected
            custom_interval = None
            if frequency == "daily":
                custom_interval = st.number_input(
                    "Custom interval (days):", min_value=1, value=1
                )
                
            # Add an input for fees per transaction
            fee = st.number_input(
                "Transaction fee ($):", min_value=0.0, value=0.0
            )    

        return ticker, investment, start_date, frequency, custom_interval, fee

    def display_dca_results_and_metrics(
        self,
        dca_results: pd.DataFrame,
        dca_array : pd.DataFrame,
        current_portfolio_value,
        percentage_increase,
    ):
        """
        Displays the DCA results and additional metrics in the right column.

        Args:
            dca_results (pd.DataFrame): The DataFrame containing DCA results to be displayed.
            total_investment (float): Total amount invested.
            current_portfolio_value (float): Current value of the portfolio.
            percentage_increase (float): Percentage increase in portfolio value.
        """
        # Display the DCA results (line chart)
        self.display_dca_results(dca_results)

        formatted_value = f"{current_portfolio_value:,.2f}".replace(",", " ")
        formatted_percentage = f"{percentage_increase:,.2f}".replace(",", " ")

        # Use in Streamlit metric
        self.col2.metric(
            "Total Investment",
            f"{formatted_value} $",
            f"{formatted_percentage}%",
        )
        
        # Display the DCA results table, using st.container to ensure full width
        st.write("### DCA Results")
        with st.container():
            st.dataframe(
                dca_array,
                use_container_width=True  # This ensures the dataframe uses full container width
            )
