import sqlite3
import os
import csv
import matplotlib
import matplotlib.pyplot as plt


# This function retrieves a list containing the symbol and price of each of the stocks from the database
def stock_lst(db_name, table_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+ db_name)
    cur = conn.cursor()

    stock_price_lst = []

    # Only retrieve the Symbol and Price information from the given table
    cur.execute('SELECT Symbol, Price From ' + table_name)
    rows = cur.fetchall()
    for i in rows:
        symbol = i[0]
        price = i[1][1:]
        if ',' in price:
            price = price.replace(',','')
        price = float(price)
        price = round(price, 2)
        stock_price_lst.append((symbol, price))
    cur.close()
    return stock_price_lst

# This function uses the stocks' price ranges to determine their affordability
def get_price_ranges(lst):
    range_lst = []
    for i in lst:
        if i[1] < 15.00:
            range_lst.append((i[0], i[1], "Low-Price"))
        elif i[1] > 15.00 and i[1] < 50.00:
            range_lst.append((i[0], i[1], "Medium-Price"))
        elif i[1] > 50.00 and i[1] < 100.00:
            range_lst.append((i[0], i[1], "Expensive"))
        else:
            range_lst.append((i[0], i[1], "Uber-Expensive"))

    return range_lst

# This function takes the information from a given list and writes it into a csv file
def write_csv(range_lst):
    with open('stock_price_ranges.csv', 'w') as stock_dump:
        write_prices = csv.writer(stock_dump, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        write_prices.writerow(["Symbol", "Price", "Affordability"])

        for i in range_lst:
            write_prices.writerow([i[0], i[1], i[2]])

# This creates a pie chart using the data of a given list with three elements
def create_pie_chart(range_lst):
    range_count = {'Low' : 0, 'Medium' : 0, 'Expensive' : 0, 'Uber-Expensive' : 0}
    for i in range_lst:
        if i[2] == "Low-Price":
            range_count['Low'] += 1
        elif i[2] == "Medium-Price":
            range_count['Medium'] += 1
        elif i[2] == "Expensive":
            range_count['Expensive'] += 1
        else:
            range_count['Uber-Expensive'] += 1

    labels = 'Low-Price', 'Medium-Price', 'Expensive', 'Uber-Expensive'
    sizes = [range_count['Low'], range_count['Medium'], range_count['Expensive'], range_count['Uber-Expensive']]
    explode = (0.1, 0.1, 0, 0)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Pie Chart of Stock Price Ranges")

    plt.savefig("stocks_pie_chart.png")
    plt.show()

def main():
    ranges = get_price_ranges(stock_lst('stocks_db.sqlite', 'Popular_Stocks'))
    write_csv(ranges)
    create_pie_chart(ranges)

if __name__ == "__main__":
    main()