import pandas as pd
import os 
from os.path import join, isdir, isfile
import datetime
import quandl
import matplotlib.pyplot as plt
import psycopg2
import subprocess

#W!1uhNIqRwwG
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
    data = pd.DataFrame()
    file_path = join(path_stock_data, ticker_name+'.csv')
    if isfile(file_path):
        data = pd.read_csv(file_path)
        existing_start_date = data['Date'].iloc[0]
        existing_end_date = data['Date'].iloc[-1]
        print(f'We already have the data for this stock {ticker_name} from date {existing_start_date} to date {existing_end_date}')
        print('Downloading......')
        data.append(quandl.get(join(source,ticker_name), start_date = start_date, end_date = end_date))
        data.drop_duplicates(['Date'],inplace=True)
        data.sort_values(by = ['Date'], inplace=True)
        data.drop([0,1,2], inplace=True)
    else:
        data = quandl.get(join(source,ticker_name), start_date = start_date, end_date = end_date)
        data.to_csv(join(path_parent, 'Stock_Data', f'{ticker_name}.csv'))
    return data
    
def writeToFile():
    pass

def drawGraph(list_x, list_y, label_x, label_y):
    plt.plot(list_x, list_y)
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.savefig(join(path_stock_data, '{ticker_name}.jpg'))

def analyzeStock():
    pass

from configparser import ConfigParser
def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
      
        # create a cursor
        cur = conn.cursor()
        
        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
 
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
        #close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def create_tables(source, ticker_name):
    """ create tables in the PostgreSQL database"""
    columns = ['Date',
               f'{source}{ticker_name}_Open',
               f'{source}{ticker_name}_High',
               f'{source}{ticker_name}_Low',
               f'{source}{ticker_name}_Close',
               f'{source}{ticker_name}_Volume',
               f'{source}{ticker_name}_Ex_Dividend',
               f'{source}{ticker_name}_Split_Ratio',
               f'{source}{ticker_name}_Adj_Open',
               f'{source}{ticker_name}_Adj_High',
               f'{source}{ticker_name}_Adj_Low',
               f'{source}{ticker_name}_Adj_Close',
               f'{source}{ticker_name}_Adj_Volume']
    commands = (
        f"""
        CREATE TABLE {ticker_name} (
            {columns[0]} date PRIMARY KEY,
            {columns[1]} float(8) ,
            {columns[2]} float(8),
            {columns[3]} float(8),
            {columns[4]} float(8),
            {columns[5]} float(8),
            {columns[6]} float(8),
            {columns[7]} float(8),
            {columns[8]} float(8),
            {columns[9]} float(8),
            {columns[10]} float(8),
            {columns[11]} float(8),
            {columns[12]} float(8)
        )
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        cur.execute(commands)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()  

def insert_vendor_list(vendor_list):
    """ insert multiple vendors into the vendors table  """
    sql = "INSERT INTO vendors(vendor_name) VALUES(%s)"
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(sql,vendor_list)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def sendtoGit(message):
    subprocess.call(['./send_to_Git.sh', message])


