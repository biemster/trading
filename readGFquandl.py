#!/usr/bin/env python
import Quandl
import matplotlib.pyplot as plt
import pickle

tseries = {}
tseries['FCF08'] = Quandl.get("CME/FCF2008", authtoken='-uJ_xVjF9qMbQ5WFUPGm')
for y in xrange(8,17):
    print 'reading 20%.2d expiry futures'%y
    for m in ['F','H','J','K','V','Q','U','V','X']:
        try: tseries['FC%s%.2d'%(m,y)] = Quandl.get('CME/FC%s20%.2d'%(m,y), authtoken='-uJ_xVjF9qMbQ5WFUPGm')
        except Quandl.Quandl.DatasetNotFound as dnf:
            print 'dataset FC%s%.2d not found'%(m,y)
            continue

pickle.dump(tseries, open( 'FeederCattleTimeseries.pickle', 'wb'))

plt.plot(tseries['FCF08'].index,tseries['FCF08'].Open)
plt.title('FCF08')
plt.show()