"""
Author: Harsha Kiran Reddy
Date: June 3 2023
"""
import mplfinance

from database import Database
from investments import Investor, Stock, Bond, load_investments_from_csv
from portfolio import load_stock_quotes_from_json, plot_stock_quote_data, create_stock_quote_dictionary, \
    plot_portfolio_data_mpl
from file_selection import FileSelectionWindow

if __name__ == '__main__':
    # File Names of the stocks, bonds, report, stocks in portfolio
    # stocks_csv_file_name = 'Lesson6_Data_Stocks.csv'
    # bonds_csv_file_name = 'Lesson6_Data_Bonds.csv'
    report_file_name = 'report.txt'
    # portfolio_stocks_json_file_name = 'AllStocks.json'
    graph_file_name = 'output.png'
    database_name = 'AllStocks.db'
    table_name = 'STOCKDATA'
    # Load stocks from the CSV file
    stocks = []

    # Select Stocks File
    try:
        file_window = FileSelectionWindow('csv', 'Select Stocks CSV file')
        stocks_csv_file_name = file_window.select_file()
        print('Selected stocks file is %s' % stocks_csv_file_name)
    except Exception as e:
        print('Exception occurred during selection of stocks csv file')

    try:
        stocks = load_investments_from_csv(stocks_csv_file_name, Stock)
    except FileNotFoundError:
        print('Stocks file not found')

    # Select Bonds File
    try:
        file_window = FileSelectionWindow('csv', 'Select Bonds CSV file')
        bonds_csv_file_name = file_window.select_file()
        print('Selected bonds file is %s' % bonds_csv_file_name)
    except Exception as e:
        print('Exception occurred during selection of stocks csv file')

    # Load bonds from the CSV file
    bonds = []
    try:
        bonds = load_investments_from_csv(bonds_csv_file_name, Bond)
    except FileNotFoundError:
        print('Bonds file not found')

    # Create an instance of the Investor class with the loaded stocks and bonds
    investor = Investor('Waren B', '007 Baker Street', '929-273-9933', stocks, bonds)
    # Create Earnings report
    investor.create_report(report_file_name)

    # Load stock_quotes for the stock in portfolio from json file.
    # Select Portfolio Json File
    try:
        file_window = FileSelectionWindow('json', 'Select Portfolio JSON file')
        portfolio_stocks_json_file_name = file_window.select_file()
        print('Selected Portfolio Json file is %s' % portfolio_stocks_json_file_name)
    except Exception as e:
        print('Exception occurred during selection of stocks csv file')
    stock_quotes = load_stock_quotes_from_json(portfolio_stocks_json_file_name)

    # Create a dictionary of those stock quotes by grouping them.
    stock_quote_dict = create_stock_quote_dictionary(stock_quotes)

    # Plot the Stock Quotes as a graph.
    plot_stock_quote_data(stock_quote_dict, stocks, graph_file_name)

    # Save the Stock Quotes to Database
    # Create Database Connection
    database = Database(database_name, table_name)
    # Create Table if not exists
    database.create_table()
    # Clear entries before loading again
    database.clear_existing_data()
    # Write the data to database
    database.write_data(stock_quotes)

    # Plot the OHLC data using mpl finance for all the stocks.
    plot_portfolio_data_mpl(portfolio_stocks_json_file_name)
