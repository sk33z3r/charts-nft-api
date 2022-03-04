from flask import Flask, send_file
from flask_cors import CORS, cross_origin
import os, time
import mplfinance as mpf
import pandas as pd
import datetime as dt
import pandas_datareader as pdr

# define the Flask app and setup CORS
app = Flask(__name__)
cors = CORS(app)

price_label = "Price ($USD)"
vol_label = "Volume"

lrc_colors = mpf.make_marketcolors(up='white',
                                   down='black',
                                   edge='inherit',
                                   wick='black',
                                   volume={ 'up': 'lightsteelblue', 'down': 'steelblue' })

lrc_style = mpf.make_mpf_style(base_mpl_style='dark_background',
                               marketcolors=lrc_colors,
                               mavcolors=['lightsteelblue', 'steelblue', 'darkblue'],
                               facecolor='dimgrey',
                               edgecolor='dimgrey',
                               figcolor='black',
                               gridcolor='darkgrey',
                               gridstyle=':',
                               gridaxis='both',
                               y_on_right=False)

gme_colors = mpf.make_marketcolors(up='white',
                                   down='black',
                                   edge='inherit',
                                   wick='black',
                                   volume={ 'up': 'darkred', 'down': 'red' })

gme_style = mpf.make_mpf_style(base_mpl_style='dark_background',
                               marketcolors=gme_colors,
                               mavcolors=['lightcoral', 'red', 'darkred'],
                               facecolor='dimgrey',
                               edgecolor='dimgrey',
                               figcolor='black',
                               gridcolor='darkgrey',
                               gridstyle=':',
                               gridaxis='both',
                               y_on_right=False)

def get_chart(stock, filename, chart_title, timeframe, averages):
    if stock == "LRC-USD":
        kwargs = dict(type='candle',
                      figscale=1,
                      figratio=(16,9),
                      title=chart_title,
                      ylabel=price_label,
                      ylabel_lower=vol_label,
                      mav=averages,
                      volume=True,
                      xrotation=20,
                      style=lrc_style,
                      savefig=filename)

    elif stock == "GME":
        kwargs = dict(type='candle',
                      figscale=1,
                      figratio=(16,9),
                      title=chart_title,
                      ylabel=price_label,
                      ylabel_lower=vol_label,
                      mav=averages,
                      volume=True,
                      show_nontrading=True,
                      xrotation=20,
                      style=gme_style,
                      savefig=filename)

    if os.path.exists(filename):
        os.remove(filename)

    now = dt.datetime.now()
    start = now - dt.timedelta(days=timeframe)

    df = pdr.get_data_yahoo(stock, start, now)
    mpf.plot(df, **kwargs)

@app.route('/lrc')
def lrc():
    lrc_file = "lrc_30_day.png"
    mav = (5, 10, 20)
    if not os.path.exists(lrc_file) or (time.time() - os.path.getmtime(lrc_file)) > 3600:
        get_chart("LRC-USD", lrc_file, "\n\nLRC-USD 30-day Candles\nwith 5-, 10-, and 20-day SMA", 31, mav)
    return send_file(lrc_file, mimetype='image/png')

@app.route('/lrc-15-day')
def lrc_15_day():
    lrc_file = "lrc_15_day.png"
    mav = 5
    if not os.path.exists(lrc_file) or (time.time() - os.path.getmtime(lrc_file)) > 3600:
        get_chart("LRC-USD", lrc_file, "\n\nLRC-USD 15-day Candles\nwith 5-day SMA", 15, mav)
    return send_file(lrc_file, mimetype='image/png')

@app.route('/lrc-5-day')
def lrc_5_day():
    lrc_file = "lrc_5_day.png"
    mav = 5
    if not os.path.exists(lrc_file) or (time.time() - os.path.getmtime(lrc_file)) > 3600:
        get_chart("LRC-USD", lrc_file, "\n\nLRC-USD 5-day Candles", 5, mav)
    return send_file(lrc_file, mimetype='image/png')

@app.route('/gme')
def gme():
    gme_file = "gme_30_day.png"
    mav = (2, 5, 10)
    if not os.path.exists(gme_file) or (time.time() - os.path.getmtime(gme_file)) > 3600:
        get_chart("GME", gme_file, "\n\nGME 30-day Candles\nwith 2-, 5-, and 10-day SMA", 30, mav)
    return send_file(gme_file, mimetype='image/png')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
