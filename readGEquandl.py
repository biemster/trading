#!/usr/bin/env python
import Quandl
import matplotlib.pyplot as plt
import pickle

tseries = {}
for y in range(25):
    print 'reading 20%.2d expiry futures'%y
    for m in ['H','M','U','Z']:
        try: tseries['ED%s%.2d'%(m,y)] = Quandl.get('CME/ED%s20%.2d'%(m,y), authtoken='-uJ_xVjF9qMbQ5WFUPGm')
        except Quandl.Quandl.DatasetNotFound as dnf:
            print 'dataset ED%s%.2d not found'%(m,y)
            continue

pickle.dump(tseries, open( 'EurodollarTimeseries.pickle', 'wb'))

plt.plot(tseries['EDH00'].index,tseries['EDH00'].Open)
plt.title('EDH00')
plt.show()