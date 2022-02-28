from flask import Flask, send_file
import os, time
import mplfinance as mpf
import pandas as pd
import datetime as dt
import pandas_datareader as pdr

app = Flask(__name__)
gme_file = "gme.png"
lrc_file = "lrc.png"

def get_chart(stock, filename, chart_title):
    kwargs = dict(type='candle', title=chart_title, mav=(3,6,9), volume=True, figratio=(11,8), figscale=0.85, style='mike', savefig=filename)

    if os.path.exists(filename):
        os.remove(filename)

    now = dt.datetime.now()
    start = now - dt.timedelta(days=30)

    df = pdr.get_data_yahoo(stock, start, now)
    mpf.plot(df, **kwargs)

@app.route('/lrc')
def lrc():
    if not os.path.exists(lrc_file) or time.time() - os.path.getmtime(filename) > (30 * 60):
        get_chart("LRC-USD", lrc_file, "LRC-USD 30-day")
    return send_file(lrc_file, mimetype='image/png')

@app.route('/gme')
def gme():
    if not os.path.exists(gme_file) or time.time() - os.path.getmtime(filename) > (30 * 60):
        get_chart("GME", gme_file, "GME 30-day")
    return send_file(gme_file, mimetype='image/png')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
