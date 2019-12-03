import pandas as pd
import os 
from os.path import join
import datetime
import quandl
import matplotlib.pyplot as plt


"""
1. path is the current directory Github/Stock_Analysis
2. parent path is the parent directory Github
3. path_stock_data is where I store the stock data locally
"""
path = os.getcwd()
path_parent = os.path.dirname(path)
path_stock_data = join(path_parent,'Stock_Data')

quandl.ApiConfig.api_key = (open(join(path_stock_data, 'quandl_key'), 'r')).readline()

#load the data either from csv files at my local folder or download it
def getStockData(source, ticker_name, start_date, end_date):
    #check if I already have the data or not
    file_path = join(path_stock_data, ticker_name+'.sql')
    if os.path.exists(file_path):
        data = pd.read_csv(file_path)
        


    data = quandl.get(join(source,ticker_name), start_date = start_date, end_date = end_date)
    return data
    

def writeToFile():
    pass

def drawGraph(list_x, list_y, label_x, label_y):
    plt.plot(list_x, list_y)
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.savefig(join(path_stock_data, 'AAPL.jpg'))
    

def run():

    end_date = datetime.datetime.today().date()
    start_date = end_date - datetime.timedelta(5000)

    print(f"The start date is {start_date}")
    print(f"The end date is {end_date}")

    names = ['TSXV/HSE']
    
    apple = getStockData(names, start_date, end_date)

    #apple = pd.read_csv(join(dir_stock_data, 'AAPL.csv'))

    drawGraph(apple['Date'], apple['WIKI/AAPL - Close'], 'Date', 'Apple stock price')

    apple.to_csv(join(upper_level_path, 'Stock_Data', f'{names[0][5:]}.csv'))

if __name__ == "__main__":
    run()