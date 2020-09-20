from bs4 import BeautifulSoup 
import requests
import sqlite3
import os

used_stocks =[]
stocks = {}

# Sets up the database and inputs the necessary data gained from the web scraping
def setUp_db(db_name, table_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS ''' + table_name + ''' (Symbol TEXT, Name TEXT, Price TEXT, Performance TEXT, Rating TEXT)''')

    # Checking for all the stocks already in the table
    cur.execute('SELECT Symbol FROM ' + table_name)
    rows = cur.fetchall()
    for i in rows:
        used_stocks.append(i[0])

    count = 0
    for i in stocks:
        # Making sure not to duplicate stocks when inputting 20 new stocks each time
        if i not in used_stocks:
            cur.execute('''INSERT INTO ''' + table_name + ''' (Symbol, Name, Price, Performance, Rating)
            VALUES ( ?, ?, ?, ?, ? )''', (stocks[i][0], stocks[i][1], stocks[i][2], stocks[i][3], stocks[i][4]) )
            conn.commit()
            count += 1
        
        # If 20 new stocks have successfully been added, end the execution of the function
        if count == 20:
            print('Finished loading data for 20 new stocks')
            break
    
    cur.close()

# Getting the data from the robinhood webpage
def robinhood_scraper(base_url):
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, "html.parser")

    # Indecing into the class that acts as the container for all the stocks' information
    for i in soup.find_all("tr", {"class":"_3-Fg9lFlzey28mCJClXXxZ"}):
        name = i.div.div.div.text
        stuff = i.find_all("td", {"class":""})
        symbol = stuff[0].a.div.span.text
        price = stuff[1].a.div.text            
        sign = ""
        deep = str(stuff[2].svg)
        triangle = deep.split('"')
        if triangle[1] != '_3fIbQm1PGrsgP3ps-22twJ _2W5gCho3Ijf6U_qtTT_A4Y':
            sign = "-"
        else:
            sign = "+"
        todays_performance = sign + stuff[2].a.div.text
        ratings = stuff[-1].a.div.text

        stocks[symbol] = ((symbol, name, price, todays_performance, ratings))


def main():
    robinhood_scraper('https://robinhood.com/collections/100-most-popular')
    setUp_db('stocks_db.sqlite', 'Popular_Stocks')

if __name__ == "__main__":
    main()