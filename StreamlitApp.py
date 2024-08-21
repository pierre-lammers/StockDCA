import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

def fetch_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

def plot_stock_data(stock_data):
    st.line_chart(stock_data['Close'])

def main():
    st.title("Application Financière DCA")
    
    ticker = st.text_input("Entrer le ticker de l'action", value="AAPL")
    start_date = st.date_input("Date de début", value=pd.to_datetime("2020-01-01"))
    end_date = st.date_input("Date de fin", value=pd.to_datetime("2023-01-01"))
    
    if st.button("Afficher les données"):
        stock_data = fetch_stock_data(ticker, start_date, end_date)
        plot_stock_data(stock_data)
    
    # Code pour DCA et calcul de p-valeur ici
    
if __name__ == "__main__":
    main()
