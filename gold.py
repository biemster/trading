#!/usr/bin/env python
import pandas
import matplotlib.pyplot as plt

if __name__ == "__main__":
    GC = ['GOLD']
    GC.append(pandas.read_csv('GOLD.csv', index_col='Date', parse_dates=True).sort_index())
    for m in range(1,11):
        # https://www.quandl.com/api/v1/datasets/CHRIS/CME_DA1.csv
        GC.append(pandas.read_csv('CME_GC%d.csv'%m, index_col='Date', parse_dates=True).sort_index())

    spreads = pandas.DataFrame(GC[1]['USD (AM)'] - GC[2]['Open'])
    spreads.rename(columns={'Open':'SPOT:FUT1'}, inplace=True)

    spreads["2016":].plot()
    plt.show()