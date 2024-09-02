from model.stock_analyzer import StockAnalyzer
from model.yahoo_provider import YahooProvider
from view.stock_view import StockView
from model.portfolio import Portfolio
from logger import get_logger
import pandas as pd
import streamlit as st

class StockController:

    portfolio = Portfolio()
    logger = get_logger(__name__)
    provider = YahooProvider()
    analyzer = StockAnalyzer()

    def __init__(self):
        self.view = StockView()  

    def run(self):
        ticker, investment, start_date, frequency, custom_interval, fee = self.view.get_user_inputs()

        if ticker:
            stock = self.provider.get_stock(ticker)

            dca_results = self.analyzer.calculate_dca(stock, investment, start_date, frequency, custom_interval, fee)

            percentage_increase = 100 * (dca_results['Portfolio Value'][-1] - dca_results['Cumulative Investment'][-1]) / dca_results['Cumulative Investment'][-1]
            
            StockController.portfolio.add_simulation_result(ticker, start_date, investment, frequency, custom_interval, percentage_increase, fee)
                
            self.clear_result()    
            
            self.view.display_dca_results_and_metrics(dca_results, StockController.portfolio.get_results(), 
                                                      current_portfolio_value=dca_results['Portfolio Value'].iloc[-1], 
                                                      percentage_increase=percentage_increase)

    def clear_result(self):
        if st.button("Clear Results"):
            self.portfolio.clear_results()