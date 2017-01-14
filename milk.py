#!/usr/bin/env python
import pandas
import matplotlib.pyplot as plt

if __name__ == "__main__":
    DA = ['milk futures']
    for m in range(1,11):
        # https://www.quandl.com/api/v1/datasets/CHRIS/CME_DA1.csv
        DA.append(pandas.read_csv('CME_DA%d.csv'%m, index_col='Date', parse_dates=True).sort())

    spreads = pandas.DataFrame(DA[1]['Settle'] - DA[2]['Settle'])
    spreads.rename(columns={'Settle':'DAs12'}, inplace=True)
    for d in range(1,10):
        if d > 1: spreads['DAs%d%d'%(d,d+1)] = pandas.Series(DA[d]['Settle'] - DA[d+1]['Settle'])
        if d < 9: spreads['DAs%d%d'%(d,d+2)] = pandas.Series(DA[d]['Settle'] - DA[d+2]['Settle'])
        if d < 8: spreads['DAs%d%d'%(d,d+3)] = pandas.Series(DA[d]['Settle'] - DA[d+3]['Settle'])
        if d < 7: spreads['DAs%d%d'%(d,d+4)] = pandas.Series(DA[d]['Settle'] - DA[d+4]['Settle'])
        if d < 6: spreads['DAs%d%d'%(d,d+5)] = pandas.Series(DA[d]['Settle'] - DA[d+5]['Settle'])
        if d < 5: spreads['DAs%d%d'%(d,d+6)] = pandas.Series(DA[d]['Settle'] - DA[d+6]['Settle'])

    spreads_1m = ['DAs12','DAs23','DAs34','DAs45','DAs56','DAs67','DAs78','DAs89']
    spreads_2m = ['DAs13','DAs24','DAs35','DAs46','DAs57','DAs68','DAs79']
    spreads_3m = ['DAs14','DAs25','DAs36','DAs47','DAs58','DAs69']
    spreads_4m = ['DAs15','DAs26','DAs37','DAs48','DAs59']
    spreads_5m = ['DAs16','DAs27','DAs38','DAs49']
    spreads_6m = ['DAs17','DAs28','DAs39']

    spreads[spreads_1m[:4]].plot()
    plt.show()
    spreads[spreads_1m[4:8]].plot()
    plt.show()
    # spreads[spreads_2m].plot()
    # plt.show()
    # spreads[spreads_3m].plot()
    # plt.show()
    # spreads[spreads_4m].plot()
    # plt.show()
    # spreads[spreads_5m].plot()
    # plt.show()
    # spreads[spreads_6m].plot()
    # plt.show()
    spreads[spreads_1m[4:8]].plot(kind='hist', alpha=0.2, xlim=[-1,1])
    plt.show()