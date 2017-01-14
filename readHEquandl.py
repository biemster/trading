#!/usr/bin/env python
import Quandl
import matplotlib.pyplot as plt
import pickle

tseries = {}
tseries['LNG08'] = Quandl.get("CME/LNG2008", authtoken='-uJ_xVjF9qMbQ5WFUPGm')
for y in xrange(8,17):
    print 'reading 20%.2d expiry futures'%y
    for m in ['G','J','K','M','N','Q','V','Z']: tseries['LN%s%.2d'%(m,y)] = Quandl.get('CME/LN%s20%.2d'%(m,y), authtoken='-uJ_xVjF9qMbQ5WFUPGm')

pickle.dump(tseries, open( 'HogsTimeseries.pickle', 'wb'))

plt.plot(tseries['LNG08'].index,tseries['LNG08'].Open)
plt.title('LNG08')
plt.show()