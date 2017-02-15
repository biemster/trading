#!/usr/bin/env python
import pandas
import matplotlib.pyplot as plt

if __name__ == "__main__":
    all_ticks = pandas.read_csv('ticks/quotesIB_20170213.txt')
    all_ticks['ts'] = pandas.DatetimeIndex((all_ticks['timestamp']*10**9) + (all_ticks['msec']*10**6))

    all_ticks_bid = (all_ticks.type == 'BID')
    all_ticks_ask = (all_ticks.type == 'ASK')
    no_empty_price = (all_ticks.price > 0)
    xauusd_symbol = (all_ticks.symbol == 'XAUUSD')
    gc1_symbol = (all_ticks.symbol == 'GCG7')
    gc2_symbol = (all_ticks.symbol == 'GCJ7')
    mgc1_symbol = (all_ticks.symbol == 'MGCG7')
    mgc2_symbol = (all_ticks.symbol == 'MGCJ7')

    xauusd_bid = pandas.Series(all_ticks[all_ticks_bid][xauusd_symbol][no_empty_price].reset_index().drop_duplicates(subset='ts', keep='last').set_index('ts').price).resample('L').pad()
    xauusd_ask = pandas.Series(all_ticks[all_ticks_ask][xauusd_symbol][no_empty_price].reset_index().drop_duplicates(subset='ts', keep='last').set_index('ts').price).resample('L').pad()

    gc1_bid = pandas.Series(all_ticks[all_ticks_bid][gc1_symbol][no_empty_price].reset_index().drop_duplicates(subset='ts', keep='last').set_index('ts').price).resample('L').pad()
    gc1_ask = pandas.Series(all_ticks[all_ticks_ask][gc1_symbol][no_empty_price].reset_index().drop_duplicates(subset='ts', keep='last').set_index('ts').price).resample('L').pad()
    
    gc2_bid = pandas.Series(all_ticks[all_ticks_bid][gc2_symbol][no_empty_price].reset_index().drop_duplicates(subset='ts', keep='last').set_index('ts').price).resample('L').pad()
    gc2_ask = pandas.Series(all_ticks[all_ticks_ask][gc2_symbol][no_empty_price].reset_index().drop_duplicates(subset='ts', keep='last').set_index('ts').price).resample('L').pad()
    
    mgc1_bid = pandas.Series(all_ticks[all_ticks_bid][mgc1_symbol][no_empty_price].reset_index().drop_duplicates(subset='ts', keep='last').set_index('ts').price).resample('L').pad()
    mgc1_ask = pandas.Series(all_ticks[all_ticks_ask][mgc1_symbol][no_empty_price].reset_index().drop_duplicates(subset='ts', keep='last').set_index('ts').price).resample('L').pad()
    
    mgc2_bid = pandas.Series(all_ticks[all_ticks_bid][mgc2_symbol][no_empty_price].reset_index().drop_duplicates(subset='ts', keep='last').set_index('ts').price).resample('L').pad()
    mgc2_ask = pandas.Series(all_ticks[all_ticks_ask][mgc2_symbol][no_empty_price].reset_index().drop_duplicates(subset='ts', keep='last').set_index('ts').price).resample('L').pad()

    print xauusd_bid
    xauusd_bid.resample("S").plot()
    gc2_bid.resample("S").plot()
    plt.show()

    (gc2_bid-xauusd_bid).resample("S").plot()
    plt.show()