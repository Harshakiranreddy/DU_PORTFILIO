"""
Author: Harsha Kiran Reddy
Date: June 3 2023
"""
from datetime import datetime
import csv


# Define the Investment class
class Investment:
    def __init__(self, symbol, shares, bought_price, current_price, purchase_date):
        self.symbol = symbol
        self.shares = int(shares)
        self.current_price = float(current_price)
        self.purchase_date = datetime.strptime(purchase_date, '%m/%d/%Y')
        self.bought_price = float(bought_price)

    # Calculate the Yearly earnings rate for an investment
    def calculate_yearly_earnings_rate(self):
        days = (datetime.now() - self.purchase_date).days
        if days == 0:
            return 0
        earnings_rate = (((self.current_price - self.bought_price) / self.bought_price) / (days / 365)) * 100
        return round(earnings_rate, 2)

    def __repr__(self):
        return "SYMBOL : %s, NO_SHARES : %s, PURCHASE_PRICE : %s, CURRENT_VALUE: %s, " \
               "PURCHASE_DATE : %s " % (self.symbol, self.shares, self.bought_price, self.current_price,
                                        self.purchase_date)


# Define the Stock class, which is a subclass of Investment
class Stock(Investment):
    pass


# Define the Bond class, which is a subclass of Investment
class Bond(Investment):
    def __init__(self, symbol, shares, bought_price, current_price, purchase_date, coupon, yield_pct):
        super().__init__(symbol, shares, bought_price, current_price, purchase_date)
        self.coupon = float(coupon)
        self.yield_pct = float(yield_pct)

    def calculate_yearly_earnings_rate(self):
        earnings_rate = super().calculate_yearly_earnings_rate()
        earnings_rate -= self.yield_pct
        return round(earnings_rate, 2)


# Investor class definition for details of the investor
class Investor:
    def __init__(self, name, address, phone, stocks, bonds):
        self.name = name
        self.address = address
        self.phone = phone
        self.stocks = stocks
        self.bonds = bonds

    def create_report(self, report_name):
        # Write the investment report to a text file
        with open(report_name, 'w') as f:
            f.write('Stocks:\n')
            f.write(f'{"Symbol":10} {"Shares":>10} {"Purchase":>20} {"Current":>20} {"Earnings":>20}\n')
            for stock in self.stocks:
                earnings = float(stock.calculate_yearly_earnings_rate())
                f.write(
                    f'{stock.symbol:10} {stock.shares:>10} {stock.bought_price:>20.2f} ${stock.current_price:>20.2f} '
                    f'{earnings:>20.2f}\n')
            f.write('\n')
            f.write('Bonds:\n')
            f.write(
                f'{"Symbol":10} {"Shares":>10} {"Purchase":>20} {"Current":>20} {"Coupon":>10} {"Yield":>10} '
                f'{"Earnings":>20}\n')
            for bond in self.bonds:
                earnings = bond.calculate_yearly_earnings_rate()
                f.write(
                    f'{bond.symbol:10} {bond.shares:>10} ${bond.bought_price:>20.2f} ${bond.current_price:>20.2f} '
                    f'{bond.coupon:>10.2f}% {bond.yield_pct:>10.2f} {earnings:>20.2f}\n')


# Define a method to load investments from a CSV file
def load_investments_from_csv(csv_file, investment_class):
    investments = []
    with open(csv_file) as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for row in reader:
            investment = investment_class(*row)
            investments.append(investment)
    return investments
