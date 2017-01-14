#!/usr/bin/env python
import Quandl
import matplotlib.pyplot as plt
import pickle

tseries = {}
tseries['LCG08'] = Quandl.get("CME/LCG2008", authtoken='-uJ_xVjF9qMbQ5WFUPGm')
for y in xrange(8,17):
    print 'reading 20%.2d expiry futures'%y
    for m in ['G','J','M','Q','V','Z']: tseries['LC%s%.2d'%(m,y)] = Quandl.get('CME/LC%s20%.2d'%(m,y), authtoken='-uJ_xVjF9qMbQ5WFUPGm')

pickle.dump(tseries, open( 'LiveCattleTimeseries.pickle', 'wb'))

plt.plot(tseries['LCG08'].index,tseries['LCG08'].Open)
plt.title('LCG08')
plt.show()