import pandas as pd
from pandas_datareader import data
import os 
from os.path import join
import datetime
import quandl
import matplotlib.pyplot as plt

cwd = os.getcwd()
upper_level_path = os.path.dirname(cwd)
dir_stock_data = join(upper_level_path,'Stock_Data')

quandl.ApiConfig.api_key = (open(join(upper_level_path, 'Stock_Data', 'quandl_key'), 'r')).readline()

#download the stock data
def getStockData(ticker_names, start_date, end_date):

    data = quandl.get(ticker_names, start_date = start_date, end_date = end_date)
    """
    data = quandl.get_table('WIKI/PRICES', ticker = ticker_names, 
                        qopts = { 'columns': ['ticker', 'date', 'close','dividend','split'] }, 
                        date = { 'gte': start_date, 'lte': end_date }, 
                        paginate=True)
    """
    return data
    

def writeToFile():
    pass

def drawGraph(list_x, list_y, label_x, label_y):
    plt.plot(list_x, list_y)
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.show()

def run():

    end_date = datetime.datetime.today().date()
    start_date = end_date - datetime.timedelta(1000)

    print(f"The start date is {start_date}")
    print(f"The end date is {end_date}")

    names = ['WIKI/AAPL']
    
    #apple = getStockData(names, start_date, end_date)

    apple = pd.read_csv(join(dir_stock_data, 'AAPL.csv'))
    drawGraph(apple['Date'], apple['WIKI/AAPL - Close'], 'Date', 'Apple stock price')

    apple.to_csv(join(upper_level_path, 'Stock_Data', f'{names[0][5:]}.csv'))

if __name__ == "__main__":
    run()