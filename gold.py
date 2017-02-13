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
    for x in xrange(1,11):
        spreads['GC%d'%x] = pandas.Series(GC[1]['USD (AM)'] - GC[x+1]['Open'])

    for x in xrange(1,11):
        print 'month ' + str(x) + ' averages:'
        for y in ['2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016']:
            print y + ': ' + str(spreads['GC%d'%x][y].mean())

    plt.show()