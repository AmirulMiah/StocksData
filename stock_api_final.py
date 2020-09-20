import json
import unittest
import os
import requests
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup 
import sqlite3
import random

#
# Your name: Shahbab Ahmed    
# Who you worked with: Amirul Miah
#


# Make sure you create an API key at alphavantage.co/support/#api-key
# Assign that to the variable API_KEY by passing in that API key

API_KEY = input("Please Enter a Valid API Key for Alpha Vantage: ")


def read_cache(CACHE_FNAME):
    """
    This function reads from the JSON cache file and returns a dictionary from the cache data.
    If the file doesn't exist, it returns an empty dictionary.
    """
    
    try:
        path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(path) 

        cache_file = open(CACHE_FNAME, 'r', encoding="utf-8") # Try to read the data from the file
        cache_contents = cache_file.read()  # If it's there, get it into a string
        CACHE_DICTION = json.loads(cache_contents) # And then load it into a dictionary
        cache_file.close() # Close the file, we're good, we got the data in a dictionary.
        return CACHE_DICTION
    except:
        CACHE_DICTION = {}
        return CACHE_DICTION

def write_cache(CACHE_FNAME, CACHE_DICT):
    """
    This function encodes the cache dictionary (CACHE_DICT) into JSON format and
    writes the JSON to the cache file (CACHE_FNAME) to save the search results.
    """
    path_to_file = os.path.join(os.path.dirname(__file__), CACHE_FNAME)
    with open(path_to_file, 'w') as f:
        f.write(json.dumps(CACHE_DICT))

# Creates the link for requesting the data by passing in the symbol of the stock
def create_request_url(symbol):
    #if symbol in nasdaq_100:
    return "https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol="+ symbol + "&" + "apikey=" + API_KEY
    #else:
    #    print("This stock is not part of the NASQAD-100 Index. Please try a different symbol")
    #    return None

def get_weekly_price_data(symbols, CACHE_FNAME):



    new_dict = read_cache(CACHE_FNAME)

    #used_lst = []
    count = 0
    #print(new_dict)
    for symbol in symbols:
        
        if symbol not in new_dict.keys():
            request_url = create_request_url(symbol)


            print("Trying to fetch data for " + symbol)
            try:
                response = urlopen(request_url)
                data = json.load(response)
                if "Weekly Time Series" in data.keys():
                    latest_date = list(data["Weekly Time Series"].keys())[0]
                    oldest_high_price = ""
                    oldest_low_price = ""

                    for i in data["Weekly Time Series"].keys():
                        if i.split("-")[0] == "2020":
                            oldest_high_price = data["Weekly Time Series"][i]["2. high"]
                            oldest_low_price = data["Weekly Time Series"][i]["3. low"]

                    

                    new_dict[symbol] = (float(data["Weekly Time Series"][latest_date]["2. high"]), float(oldest_high_price), float(data["Weekly Time Series"][latest_date]["3. low"]), float(oldest_low_price))
                    write_cache(CACHE_FNAME, new_dict)

                     
                    print("Successfully fetched data for " + symbol)
                    count += 1

                    if count == 20:
                        break
                
            except:
                print("None")
        else:
            print("The data for " + symbol + " has already been stored.")

        '''for i in data["Weekly Time Series"].keys():
            if i.split("-")[0] == "2020":
                
                if 
                new_dict[symbol] = data["Weekly Time Series"][i]
                #print(new_dict)'''

        
                
    
            #else:
            #    print(data["Error"])
    print("Finished loading data for " + str(count) + " new stocks. Total of " + str(len(new_dict)) + " stocks loaded.")
    
    return new_dict


#conn = sqlite3.connect('/Users/shahbaba/Desktop/SI206/FinalProjectStock/stocks_database.sqlite')
#cur = conn.cursor()

#cur.execute('''
#CREATE TABLE IF NOT EXISTS Stocks (Symbol TEXT, LatestWeekPrice TEXT, OldestWeekPrice TEXT)''')


def create_db_high(stock_dict, db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS Stocks_High (Symbol TEXT, HighLatestWeekPrice TEXT, HighOldestWeekPrice TEXT)''')

    #used_stocks = read_cache("used_stocks.json")
    cur.execute('SELECT Symbol FROM Stocks_High')

    rows = cur.fetchall()

    rows_lst = []
    for i in rows:
        rows_lst.append(i[0])
    #print(rows_lst)
    #print(used_stocks)
    for i in stock_dict:
    #    if i not in used_stocks:
    #        used_stocks.append(i)





        #print((rows))

        if i not in rows_lst:
            cur.execute('''INSERT INTO Stocks_High (Symbol, HighLatestWeekPrice, HighOldestWeekPrice)
                    VALUES ( ?, ?, ?)''', (i, stock_dict[i][0], stock_dict[i][1]) ) 
            conn.commit()
    
def create_db_low(stock_dict, db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS Stocks_Low (Symbol TEXT, LowLatestWeekPrice TEXT, LowOldestWeekPrice TEXT)''')

    #used_stocks = read_cache("used_stocks.json")
    cur.execute('SELECT Symbol FROM Stocks_Low')

    rows = cur.fetchall()

    rows_lst = []

    for i in rows:
        rows_lst.append(i[0])
    #print(rows_lst)
    #print(used_stocks)
    for i in stock_dict:
    #    if i not in used_stocks:
    #        used_stocks.append(i)





        #print((rows))

        if i not in rows_lst:
            cur.execute('''INSERT INTO Stocks_Low (Symbol, LowLatestWeekPrice, LowOldestWeekPrice)
                    VALUES ( ?, ?, ?)''', (i, stock_dict[i][2], stock_dict[i][3]) ) 
            conn.commit()



'''def create_symbols():
    base_url = 'https://robinhood.com/collections/100-most-popular'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, "html.parser")
    
    symbols = []

    for i in soup.find_all("tr", {"class":"_3-Fg9lFlzey28mCJClXXxZ"}):
        stuff = i.find_all("td", {"class":""})
        symbol = stuff[0].a.div.span.text
        symbols.append(symbol)
    
    return symbols'''

#sam = {'AACG': ('0.8500', '1.4892'), 'AAL': ('11.3500', '29.2950'), 'AAME': ('1.9500', '2.0989'), 'AAOI': ('8.6520', '12.5300'), 'AAON': ('47.5000', '50.4200'), 'AKTX': ('1.6300', '1.8000'), 'ALAC': ('10.4700', '10.3500'), 'ALACR': ('0.1800', '0.2200'), 'ALACU': ('10.4900', '10.6500'), 'ALACW': ('0.0300', '0.0800'), 'ALBO': ('19.1000', '26.7100')}


def create_symbols(fname):

    path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(path) 
    
    text_file = open(fname, "r")
    lines = text_file.readlines()

    #Randomizes stocks
    random.shuffle(lines)
    
    text_file.close()
    
    symbols = []
    for i in lines:
        
        i = i.split("|")[0]

        symbols.append(i)
    #symbols.pop(-1)
    return symbols
    
#print(create_symbols())


#for i in range(10):

#get_weekly_price_data(create_symbols(), "stock_data.json")

#print(read_cache("stock_data.json"))

#print(create_request_url("CHKP"))
#print(create_request_url("CHK"))

#get_data_with_caching(create_symbols(), "stock_data")



    
stocks_dict = get_weekly_price_data(create_symbols("nasdaqlisted.txt"), "stock_data.json")

create_db_high(stocks_dict, "stocks_db.sqlite")
create_db_low(stocks_dict, "stocks_db.sqlite")


#def main():

    

    #get_weekly_price_data(create_symbols(), "stock_data.json")
    
    #create_high_database(stocks, "stocks.sqlite")
        #get_weekly_price_data(create_symbols(), "stock_data.json")


#if __name__ == "__main__":
#    main()
    
#    unittest.main(verbosity=2)