import pandas as pd
from pandas_datareader import data
import os 
from os.path import join
import datetime
import quandl

cwd = os.getcwd()
upper_level_path = os.path.dirname(cwd)
print(upper_level_path)

quandl.ApiConfig.api_key = (open(join(upper_level_path, 'Stock_Data', 'quandl_key'), 'r')).readline()

#download the stock data
def getStockData(ticker_name, start_date, end_date):
    tickers = []
    tickers.append(ticker_name)
    data = quandl.get_table('WIKI/PRICES', ticker = tickers, 
                        qopts = { 'columns': ['ticker', 'date', 'adj_close'] }, 
                        date = { 'gte': start_date, 'lte': end_date }, 
                        paginate=True)
    return data
    

def writeToFile():
    pass

def run():

    end_date = datetime.datetime.today().date()
    start_date = end_date - datetime.timedelta(1000)

    print(f"The start date is {start_date}")
    print(f"The end date is {end_date}")

    husky = getStockData('AAPL', start_date, end_date)
    print(husky)

if __name__ == "__main__":
    run()