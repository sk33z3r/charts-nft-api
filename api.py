from flask import Flask, send_file
import matplotlib.pyplot as plt
import pandas as pd
import os, time

app = Flask(__name__)
filename = "chart.png"

def gen_chart():
    os.remove(filename)

    #create DataFrame
    prices = pd.DataFrame({'open': [25, 22, 21, 19, 23, 21, 25, 29],
                        'close': [24, 20, 17, 23, 22, 25, 29, 31],
                        'high': [28, 27, 29, 25, 24, 26, 31, 37],
                        'low': [22, 16, 14, 17, 19, 18, 22, 26]},
                        index=pd.date_range("2021-01-01", periods=8, freq="d"))

    #create figure
    plt.figure()

    #define width of candlestick elements
    width = .4
    width2 = .05

    #define up and down prices
    up = prices[prices.close>=prices.open]
    down = prices[prices.close<prices.open]

    #define colors to use
    col1 = 'green'
    col2 = 'red'

    #plot up prices
    plt.bar(up.index,up.close-up.open,width,bottom=up.open,color=col1)
    plt.bar(up.index,up.high-up.close,width2,bottom=up.close,color=col1)
    plt.bar(up.index,up.low-up.open,width2,bottom=up.open,color=col1)

    #plot down prices
    plt.bar(down.index,down.close-down.open,width,bottom=down.open,color=col2)
    plt.bar(down.index,down.high-down.open,width2,bottom=down.open,color=col2)
    plt.bar(down.index,down.low-down.close,width2,bottom=down.close,color=col2)

    #rotate x-axis tick labels
    plt.xticks(rotation=45, ha='right')

    #save the candlestick chart
    plt.savefig(filename)


@app.route('/')
def index():
    if time.time() - os.path.getmtime(filename) > (5 * 3):
        gen_chart()
    return send_file(filename, mimetype='image/png')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
