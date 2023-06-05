"""
Author: Harsha Kiran Reddy
Date: June 3 2023
"""
import sqlite3
from datetime import datetime


class Database:
    def __init__(self, database, table):
        self.database = database
        self.table = table
        self.conn = sqlite3.connect(database)

    def create_table(self):
        # SQL statement to create a table if it doesn't exist
        ddl_create_table = """CREATE TABLE IF NOT EXISTS %s (
                            SYMBOL TEXT NOT NULL, 
                            STOCK_DATE TEXT NOT NULL, 
                            OPEN_PRICE NUMERIC NOT NULL, 
                            HIGH_PRICE NUMERIC NOT NULL, 
                            LOW_PRICE NUMERIC NOT NULL, 
                            CLOSE_PRICE NUMERIC NOT NULL, 
                            VOLUME INT NOT NULL);""" % self.table
        # Execute the create table statement
        self.conn.execute(ddl_create_table)
        # Commit the changes
        self.conn.commit()

    def clear_existing_data(self):
        # Delete all rows from the table
        self.conn.execute('DELETE from %s' % self.table)
        # Commit the changes
        self.conn.commit()

    def write_data(self, stock_quotes):
        for stock_quote in stock_quotes:
            # Prepare the insert statement with the stock quote data
            insert_dml = "INSERT INTO %s (SYMBOL, STOCK_DATE, OPEN_PRICE, " \
                         "HIGH_PRICE, LOW_PRICE, CLOSE_PRICE, VOLUME) " \
                         "VALUES (  '%s',  '%s',  '%s',  '%s',  '%s',  '%s',  '%s')" % (
                             self.table, stock_quote['Symbol'], datetime.strptime(stock_quote['Date'], "%d-%b-%y"),
                             stock_quote['Open'], stock_quote['High'],
                             stock_quote['Low'], stock_quote['Close'], stock_quote['Volume'])
            # Execute the insert statement
            self.conn.execute(insert_dml)
            # Commit the changes
        self.conn.commit()
