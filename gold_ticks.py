#!/usr/bin/env python
import glob
import pandas
import matplotlib.pyplot as plt

if __name__ == "__main__":
    all_ticks = pandas.concat([pandas.read_csv(f) for f in glob.glob('ticks/quotesIB*')], ignore_index=True)
    all_ticks['ts'] = pandas.DatetimeIndex((all_ticks['timestamp']*10**9) + (all_ticks['msec']*10**6))

    all_ticks_bid = (all_ticks.type == 'BID')
    all_ticks_ask = (all_ticks.type == 'ASK')
    no_empty_price = (all_ticks.price > 0)
    xauusd_symbol = (all_ticks.symbol == 'XAUUSD')
    gc1_symbol = (all_ticks.symbol == 'GCG7')
    gc2_symbol = (all_ticks.symbol == 'GCJ7')
    mgc1_symbol = (all_ticks.symbol == 'MGCG7')
    mgc2_symbol = (all_ticks.symbol == 'MGCJ7')

    xauusd_bid = pandas.Series(all_ticks[all_ticks_bid][xauusd_symbol][no_empty_price]
                        .reset_index().drop_duplicates(subset='ts', keep='last').set_index('ts').price)
                        # .resample('L').pad()
    xauusd_ask = pandas.Series(all_ticks[all_ticks_ask][xauusd_symbol][no_empty_price]
                        .reset_index().drop_duplicates(subset='ts', keep='last').set_index('ts').price)
                        # .resample('L').pad()

    gc1_bid = pandas.Series(all_ticks[all_ticks_bid][gc1_symbol][no_empty_price]
                        .reset_index().drop_duplicates(subset='ts', keep='last').set_index('ts').price)
                        # .resample('L').pad()
    gc1_ask = pandas.Series(all_ticks[all_ticks_ask][gc1_symbol][no_empty_price]
                        .reset_index().drop_duplicates(subset='ts', keep='last').set_index('ts').price)
                        # .resample('L').pad()
    
    gc2_bid = pandas.Series(all_ticks[all_ticks_bid][gc2_symbol][no_empty_price]
                        .reset_index().drop_duplicates(subset='ts', keep='last').set_index('ts').price)
                        # .resample('L').pad()
    gc2_ask = pandas.Series(all_ticks[all_ticks_ask][gc2_symbol][no_empty_price]
                        .reset_index().drop_duplicates(subset='ts', keep='last').set_index('ts').price)
                        # .resample('L').pad()
    
    mgc1_bid = pandas.Series(all_ticks[all_ticks_bid][mgc1_symbol][no_empty_price]
                        .reset_index().drop_duplicates(subset='ts', keep='last').set_index('ts').price)
                        # .resample('L').pad()
    mgc1_ask = pandas.Series(all_ticks[all_ticks_ask][mgc1_symbol][no_empty_price]
                        .reset_index().drop_duplicates(subset='ts', keep='last').set_index('ts').price)
                        # .resample('L').pad()
    
    mgc2_bid = pandas.Series(all_ticks[all_ticks_bid][mgc2_symbol][no_empty_price]
                        .reset_index().drop_duplicates(subset='ts', keep='last').set_index('ts').price)
                        # .resample('L').pad()
    mgc2_ask = pandas.Series(all_ticks[all_ticks_ask][mgc2_symbol][no_empty_price]
                        .reset_index().drop_duplicates(subset='ts', keep='last').set_index('ts').price)
                        # .resample('L').pad()

    # xauusd_bid.resample("5T").plot()
    # gc2_bid.resample("5T").plot()
    (gc2_ask.resample('30S') - xauusd_bid.resample('30S')).plot()
    (gc2_bid.resample('30S') - xauusd_ask.resample('30S')).plot()
    plt.show()

    day = '2017-02-08'
    median = ((gc2_ask[day].resample('L').pad() - xauusd_bid[day].resample('L').pad())
           + (gc2_bid[day].resample('L').pad() - xauusd_ask[day].resample('L').pad())).dropna() / 2

    print median.min()
    print median.mean()
    print median.max()
    median.hist()
    plt.show()

    median[median < 0].resample('30S').plot()
    plt.show()