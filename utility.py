import pandas as pd
from pandas_datareader import data
import os 
from os.path import join
import datetime
import quandl

quandl.ApiConfig.api_key = 'FbG6tRQrs3qMtkGBrhZ5'

cwd = os.getcwd()
quandl_key = 'FbG6tRQrs3qMtkGBrhZ5'

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