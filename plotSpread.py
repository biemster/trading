#!/usr/bin/env python
import sys
import pickle
import pandas
from pandas.tseries.offsets import DateOffset
import matplotlib.pyplot as plt

month = {'F':'Jan', 'G':'Feb', 'H':'Mar', 'J':'Apr', 'K':'May', 'M':'Jun', 'N':'Jul', 'Q':'Aug', 'U':'Sep', 'V':'Oct', 'X':'Nov', 'Z':'Dec'}
dname = {'DA':'Milk', 'LN':'Hogs', 'LC':'LiveCattle', 'FC':'FeederCattle', 'ED':'Eurodollar'}
ystart = {'DA':11, 'LN':8, 'LC':8, 'FC':8, 'ED':0}
lastyear = {'DA':17, 'LN':17, 'LC':17, 'FC':16, 'ED':18}
dmonths = { 'DA':['F','G','H','J','K','M','N','Q','U','V','X','Z'],
            'LN':['G','J','K','M','N','Q','V','Z'],
            'LC':['G','J','M','Q','V','Z'],
            'FC':['F','H','J','K','V','Q','U','V','X'],
            'ED':['H','M','U','Z']}
ndaysinplot = 800

def plotSeries(s, fold):
    printout = dname[s[:2]] + ':'
    for m in dmonths[s[:2]]: printout = '%s %s:%s,' % (printout,month[m],m)
    print printout
    
    fname = dname[s[:2]] + 'Timeseries.pickle'

    tseries = pickle.load(open(fname,'rb'))
    for y in range(ystart[s[:2]], lastyear[s[:2]]):
        if len(s) == 3 and y<lastyear[s[:2]]-1:
            spread = pandas.Series(tseries[s[:3] + '%.2d'%y].Settle
                                 - tseries[s[:3] + '%.2d'%(y+1)].Settle)
        if len(s) == 4:
            spread = pandas.Series(tseries[s[:3] + '%.2d'%y].Settle
                                 - tseries[s[:2] + s[3] + '%.2d'%y].Settle)
        if len(s) == 5 and y<lastyear[s[:2]]-1:
            # Eurodollar butterflies
            yplus = 0;
            if s[2] == 'U' or s[2] == 'Z': yplus = 1    # UHU or ZMZ fly
            spread = pandas.Series(1*tseries[s[:3] + '%.2d'%y].Settle
                                  -2*tseries[s[:2] + s[3] + '%.2d'%(y+yplus)].Settle
                                  +1*tseries[s[:2] + s[4]+ '%.2d'%(y+1)].Settle)
        if len(s) == 6 and y<lastyear[s[:2]]-1:
            # Eurodollar double butterflies
            yplus = 0;
            if s[2] == 'U' or s[2] == 'Z': yplus = 1    # UHU or ZMZ fly
            spread = pandas.Series(1*tseries[s[:3] + '%.2d'%y].Settle
                                  -3*tseries[s[:2] + s[3] + '%.2d'%(y+yplus)].Settle
                                  +3*tseries[s[:2] + s[4]+ '%.2d'%(y+1)].Settle
                                  -1*tseries[s[:2] + s[5]+ '%.2d'%(y+1)].Settle)
        
        if fold:
            today = pandas.to_datetime('today')
            spread.index = spread.index - DateOffset(years=(y+2000)-today.year)
            spread -= spread[today:today + DateOffset(days=2)].mean()
            try: spread[today:].dropna().plot(ax=axes[1])
            except TypeError: print 'no data for 20%.2d'%y
            axes[1].grid(b=True, which='both', color='gray', linestyle='--')
        else:
            spread[-ndaysinplot:].plot(ax=axes[0])
            axes[0].grid(b=True, which='both', color='gray', linestyle='--')
    
    if len(s) == 3: axes[0].set_title(dname[s[:2]] + ' ' + month[s[2]] + '/' + month[s[2]] + '+1y')
    if len(s) == 4: axes[0].set_title(dname[s[:2]] + ' ' + month[s[2]] + '/' + month[s[3]])
    if len(s) >= 5: axes[0].set_title(dname[s[:2]] + ' ' + s[2:])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        printout = 'monthcodes:'
        for m in month: printout = '%s %s:%s,' % (printout,month[m],m)
        print printout
    else:
        fig, axes = plt.subplots(nrows=2, ncols=1)
        fig.tight_layout()
        
        plotSeries(sys.argv[1], False);
        axes[0].axhline(y=0, xmin=0, xmax=1, linewidth=2, color='red', linestyle='--')
        # pandas.read_csv('CME_DA1.csv', index_col='Date', parse_dates=True).Settle.plot(ax=axes[0].twinx())
        
        plotSeries(sys.argv[1], True);
        axes[1].axhline(y=0, xmin=0, xmax=1, linewidth=2, color='red', linestyle='--')
        
        plt.show()
