"""
Author: Harsha Kiran Reddy
Date: June 3 2023
"""
import json
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf


# Class to store the Stock Quotes of a specific Stock.
class StockQuotes:
    def __init__(self, symbol):
        self.symbol = symbol
        self.dates = []
        self.open_prices = []
        self.high_prices = []
        self.low_prices = []
        self.close_prices = []
        self.volumes = []

    # Function to add a Quote to the Stock.
    def add_quote(self, date, open_price, high_price, low_price, close_price, volume):
        self.dates.append(datetime.strptime(date, '%d-%b-%y'))
        self.open_prices.append(open_price)
        self.high_prices.append(high_price)
        self.low_prices.append(low_price)
        self.close_prices.append(close_price)
        self.volumes.append(volume)


# Method to read the stock quotes from json file.
def load_stock_quotes_from_json(json_file):
    # open the json file
    f = open(json_file)
    # load the json content
    stock_quotes_in_json = json.load(f)
    f.close()
    return stock_quotes_in_json


# create a dictionary of stock quotes combining the quotes by a symbol.
def create_stock_quote_dictionary(stock_quotes_in_json):
    # Dictionary which will store the quotations for a stock ex: {'GOOGL':StockQuote}
    stock_quote_dict = {}
    for stock_quote in stock_quotes_in_json:
        symbol = stock_quote['Symbol']
        if symbol.__eq__('GOOG'):
            symbol = 'GOOGL'
        if stock_quote_dict.get(symbol) is None:
            stock_quote_dict[symbol] = StockQuotes(symbol)
        stock_quote_dict[symbol].add_quote(stock_quote['Date'], stock_quote['Open'],
                                           stock_quote['High'], stock_quote['Low'], stock_quote['Close'],
                                           stock_quote['Volume'])
    return stock_quote_dict


def plot_stock_quote_data(stock_quote_dict, stocks, graph_name):
    # Set the size of the Graph
    plt.figure(figsize=(30, 18))

    # Plot the Stocks Performance
    for stock in stocks:
        # Get the closing price of a stock
        closing_prices = stock_quote_dict[stock.symbol].close_prices
        # Get the value of investment on a date by multiplying number of shares with closing price of the stock
        number_of_shares = stock.shares
        stock_investment_values = [closing_price * number_of_shares for closing_price in closing_prices]
        # Get the dates of the Quotes
        dates = stock_quote_dict[stock.symbol].dates

        try:
            # Plot the Data
            plt.plot(dates, stock_investment_values, label=stock.symbol)
        except KeyError as e:
            print("Error plotting graph:", e)

        # Set Labels, Title and Legend
        plt.xlabel("Date")
        plt.ylabel("Investment Value")
        plt.title("Investment Performance")
        plt.legend(title='Stocks')

        # Format the Dates on X-Axis
        plt.gcf().autofmt_xdate()

        # Save the plot
        plt.savefig(graph_name)


def plot_portfolio_data_mpl(portfolio_stocks_json_file_name):
    df = pd.read_json(portfolio_stocks_json_file_name)
    df['Date'] = pd.to_datetime(df['Date'])
    # clean up rows which have '-' in Open, Close, Low, High.
    df = df[(df.Open != '-')]
    df = df[(df.Close != '-')]
    df = df[(df.Low != '-')]
    df = df[(df.High != '-')]
    # Convert Open, Close, Low, High columns as float
    df['Open'] = df['Open'].astype(float)
    df['Close'] = df['Close'].astype(float)
    df['Low'] = df['Low'].astype(float)
    df['High'] = df['High'].astype(float)
    df_grouped = df.groupby(df.Symbol)
    for group in df_grouped.groups:
        df1 = df_grouped.get_group(group)
        df1 = df1.set_index('Date')
        mpf.plot(df1, type='line',
                 savefig=group + ".jpg")
