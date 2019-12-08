from Stock_Analysis.utility import getStockData, drawGraph, analyzeStock
from datetime import datetime

def run():
    user_condition = True
    user_interface = {}
    while(user_condition):
        print("What operation do you want to perform: ")
        print("a: Download Stock Data")
        print("b: Visualize Stock Data")
        print("c: Analyze Stock Data")
        print("e: Exit this user interface")
        user_input = input()
        if user_input == 'a':
            end_date = datetime.datetime.today().date()
            start_date = end_date - datetime.timedelta(5000)
            print(f"The start date is {start_date}")
            print(f"The end date is {end_date}")
            source = 'WIKI'
            ticker_name = 'AAPL'
            apple = getStockData(source, ticker_name, start_date, end_date)
            print(apple.head())
            print(apple.columns)
        elif user_input == 'b':
            drawGraph()
        elif user_input == 'c':
            analyzeStock()
        elif user_input == 'e':
            user_condition = False
            print('exiting')
        else:
            print(f'You have entered invalid input, {user_input}')
            user_condition = True

    #apple = pd.read_csv(join(dir_stock_data, 'AAPL.csv'))
    #drawGraph(apple['Date'], apple['WIKI/AAPL - Close'], 'Date', 'Apple stock price')

if __name__ == "__main__":
    run()