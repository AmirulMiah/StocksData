import sqlite3
import os
import csv
import matplotlib
import matplotlib.pyplot as plt, numpy as np
#import numpy as np
#import matplotlib.ticker as ticker

def join_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()

    cur.execute("SELECT * FROM Stocks_High JOIN Stocks_Low ON Stocks_High.Symbol = Stocks_Low.Symbol")

    return (cur.fetchall())

#print(join_database("stocks_db.sqlite"))

def calculate_net_price(db_lst):

    net_price_lst = []
    for i in db_lst:
        net_price_lst.append((i[0], round(float(i[1]) - float(i[2]), 2), round(float(i[4]) - float(i[5]), 2)))

    return net_price_lst


def write_csv(net_lst, file_name):
    path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(path) 

    with open(file_name, 'w') as stock_file:
        write_prices = csv.writer(stock_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        write_prices.writerow(["Symbol", "Net High Price", "Net Low Price"])

        for i in net_lst:
            write_prices.writerow([i[0], i[1], i[2]])


def create_scatterplot_high_low(net_lst):

    x = []
    y = []
    for i in net_lst:
        #color_dict = {i[1]: "green", i[2]: "blue"}
        x.append(i[1])
        y.append(i[2])
        #y = i[1]
    plt.scatter(x, y)
    
    plt.title("Scatterplot of Net High Prices by Net Low Prices")
    plt.xlabel("Net High Prices: Latest - First (Week of 2020)")
    plt.ylabel("Net Low Prices: Latest - First (Week of 2020)")

    plt.savefig("scatterplot_high_low.png")
    plt.show()

def create_pie_chart(net_lst, low_or_high):
    range_count = {'Negative' : 0, 'Positive' : 0, 'Equal' : 0}
    
    if low_or_high.upper() == "HIGH":
        for i in net_lst:
            if i[1] < 0:
                range_count['Negative'] += 1
            elif i[1] > 0:
                range_count['Positive'] += 1
            elif i[1] == 0:
                range_count['Equal'] += 1
    elif low_or_high.upper() == "LOW":
        for i in net_lst:
            if i[2] < 0:
                range_count['Negative'] += 1
            elif i[2] > 0:
                range_count['Positive'] += 1
            elif i[2] == 0:
                range_count['Equal'] += 1
    else:
        print("Please choose to either plot High Net Prices by using 'high' or Low Net Prices by using 'low'")
        return
        
    labels = 'Net Negative', 'Net Positive', 'Net Equal'
    sizes = [range_count['Negative'], range_count['Positive'], range_count['Equal']]
    #explode = (0.1, 0.1, 0, 0)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes,  labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    if low_or_high.upper() == "HIGH":
        plt.title("Pie Chart of Net High Stock Prices (Latest - First Week of 2020)")
        plt.savefig("stocks_pie_chart_high.png")

    elif low_or_high.upper() == "LOW":
        plt.title("Pie Chart of Net Low Stock Prices (Latest - First Week of 2020)")
        plt.savefig("stocks_pie_chart_low.png")



    plt.show()

#create_pie_chart(lst)
'''def create_pie_chart_low(net_lst):
    range_count = {'Negative' : 0, 'Positive' : 0, 'Equal' : 0}
    for i in net_lst:
        if i[2] < 0:
            range_count['Negative'] += 1
        elif i[2] > 0:
            range_count['Positive'] += 1
        elif i[2] == 0:
            range_count['Equal'] += 1
        
    labels = 'Net Negative', 'Net Positive', 'Net Equal'
    sizes = [range_count['Negative'], range_count['Positive'], range_count['Equal']]
    #explode = (0.1, 0.1, 0, 0)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes,  labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Pie Chart of Net Low Stock Prices (Latest - First Week of 2020)")

    plt.savefig("stocks_pie_chart_low.png")
    plt.show()'''

print(len(join_database("stocks_db.sqlite")))
lst = calculate_net_price(join_database("stocks_db.sqlite"))
print(len(lst))
write_csv(lst, "stock_net_prices.csv")
create_scatterplot_high_low(lst)
create_pie_chart(lst, "high")
create_pie_chart(lst, "Low")
#create_pie_chart(lst, "med")