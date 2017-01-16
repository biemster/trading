#!/usr/bin/env python
import pickle
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

tseries = pickle.load(open('EurodollarTimeseries.pickle','rb'))

dates = []
for y in [12,13,14]:
    for m in range(1,13):
        if y==14 and m>11: break
        dates.append( str(tseries['EDM17'].ix['20%d-%0d-01'%(y,m):'20%d-%0d-05'%(y,m),'Open'].index[0])[:10] )

with PdfPages('EurodollarSpreads.pdf') as pdf:
    for date in dates:
        print 'making plot for', date
        currentYear = int(date[2:4])
        HMUZ = []
        if int(date[5:7]) <  3: HMUZ.append(['EDH%d'%currentYear, tseries['EDH%d'%currentYear].ix[date,'Open']])
        if int(date[5:7]) <  6: HMUZ.append(['EDM%d'%currentYear, tseries['EDM%d'%currentYear].ix[date,'Open']])
        if int(date[5:7]) <  9: HMUZ.append(['EDU%d'%currentYear, tseries['EDU%d'%currentYear].ix[date,'Open']])
        if int(date[5:7]) < 12: HMUZ.append(['EDZ%d'%currentYear, tseries['EDZ%d'%currentYear].ix[date,'Open']])
        for t in range(currentYear+1,currentYear+5):
            for m in ['H','M','U','Z']:
                fut = 'ED%s%d' % (m,t)
                try: HMUZ.append([fut, tseries[fut].ix[date,'Open']])
                except KeyError: print 'KeyError in', fut
        if int(date[5:7]) >  2: HMUZ.append(['EDH%d'%(currentYear+6), tseries['EDH%d'%(currentYear+6)].ix[date,'Open']])
        if int(date[5:7]) >  5: HMUZ.append(['EDM%d'%(currentYear+6), tseries['EDM%d'%(currentYear+6)].ix[date,'Open']])
        if int(date[5:7]) >  8: HMUZ.append(['EDU%d'%(currentYear+6), tseries['EDU%d'%(currentYear+6)].ix[date,'Open']])
        if int(date[5:7]) > 11: HMUZ.append(['EDZ%d'%(currentYear+6), tseries['EDZ%d'%(currentYear+6)].ix[date,'Open']])

        pPlot1 = []
        pPlot2 = []
        pPlot3 = []
        pPlot4 = []
        fPlot = []
        for i in range(len(HMUZ)-4):
            fPlot.append(HMUZ[i][0])
            pPlot1.append(HMUZ[i][1]-HMUZ[i+1][1])
            pPlot2.append(HMUZ[i][1]-HMUZ[i+2][1])
            pPlot3.append(HMUZ[i][1]-HMUZ[i+3][1])
            pPlot4.append(HMUZ[i][1]-HMUZ[i+4][1])

        from matplotlib import pyplot as plt
        import numpy as np
        w = .2
        plus3m = plt.bar(np.arange(len(fPlot))-2*w, pPlot1, width=w, color='r', align='center')
        plus6m = plt.bar(np.arange(len(fPlot))-w,   pPlot2, width=w, color='g', align='center')
        plus9m = plt.bar(np.arange(len(fPlot)),     pPlot3, width=w, color='b', align='center')
        plus1y = plt.bar(np.arange(len(fPlot))+w,   pPlot4, width=w, color='m', align='center')
        plt.xticks(np.arange(len(fPlot)), fPlot, rotation='vertical')
        plt.yticks(np.arange(0,1.5,.1))
        plt.legend( (plus3m[0], plus6m[0], plus9m[0], plus1y), ('+3M futures (H,M)', '+6M futures (H,U)', '+9M futures (H,Z)', '+1Y futures (Hn,Hn+1)') )
        plt.title('eurodollar spreads %s Open' % date)
        plt.axes().yaxis.grid(True, 'both')
        pdf.savefig(bbox_inches='tight')
        plt.close()
