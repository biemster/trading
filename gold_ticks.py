#!/usr/bin/env python
import pandas
import matplotlib.pyplot as plt

if __name__ == "__main__":
    all_ticks = pandas.read_csv('ticks/quotesIB_20170206.txt')
    all_ticks['ts'] = pandas.DatetimeIndex((all_ticks['timestamp']*10**9) + (all_ticks['msec']*10**6))

    all_ticks_bid = (all_ticks.type == 'BID')
    all_ticks_ask = (all_ticks.type == 'ASK')
    no_empty_price = (all_ticks.price > 0)
    xauusd_symbol = (all_ticks.symbol == 'XAUUSD')

    xauusd_bid = pandas.Series(all_ticks[all_ticks_bid][xauusd_symbol][no_empty_price].reset_index().drop_duplicates(subset='ts', keep='last').set_index('ts').price)
    xauusd_ask = pandas.Series(all_ticks[all_ticks_ask][xauusd_symbol][no_empty_price].reset_index().drop_duplicates(subset='ts', keep='last').set_index('ts').price)

    print xauusd_bid
    xauusd_bid.plot()
    xauusd_ask.plot()
    plt.show()