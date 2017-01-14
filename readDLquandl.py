#!/usr/bin/env python
import Quandl
import matplotlib.pyplot as plt
import pickle

tseries = {}
tseries['DAG11'] = Quandl.get("CME/DAG2011", authtoken='-uJ_xVjF9qMbQ5WFUPGm')
for y in xrange(11,17):
    print 'reading 20%.2d expiry futures'%y
    for m in ['F','G','H','J','K','M','N','Q','U','V','X','Z']: tseries['DA%s%.2d'%(m,y)] = Quandl.get('CME/DA%s20%.2d'%(m,y), authtoken='-uJ_xVjF9qMbQ5WFUPGm')

pickle.dump(tseries, open( 'MilkTimeseries.pickle', 'wb'))

plt.plot(tseries['DAG11'].index,tseries['DAG11'].Open)
plt.title('DAG11')
plt.show()