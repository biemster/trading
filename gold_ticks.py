#!/usr/bin/env python
import pandas
import matplotlib.pyplot as plt

if __name__ == "__main__":
    all_ticks = pandas.read_csv('ticks/quotesIB_20170206.txt')
    all_ticks['ts'] = pandas.DatetimeIndex((all_ticks['timestamp']*10**9) + (all_ticks['msec']*10**6))

    all_ticks_bid = (all_ticks.type == 'BID')
    all_ticks_ask = (all_ticks.type == 'ASK')
    xauusd_symbol = (all_ticks.symbol == 'XAUUSD')

    xauusd_bid = pandas.Series(all_ticks[all_ticks_bid][xauusd_symbol].price)

    print all_ticks[all_ticks_bid][xauusd_symbol]
    print xauusd_bid