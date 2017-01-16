#!/usr/bin/env python
import pickle
import matplotlib.pyplot as plt
import numpy as np

tseries = pickle.load(open('EurodollarTimeseries.pickle','rb'))
nextExpiryPerMonth = {1:'H', 2:'H', 3:'M', 4:'M', 5:'M', 6:'U', 7:'U', 8:'U', 9:'Z', 10:'Z', 11:'Z', 12:'H'}
nextQ = {'H':'M', 'M':'U', 'U':'Z', 'Z':'H'}
testDate = '2014-11-19'

# fill the spreadCurve for every available date
spreadCurve = {}
nValues = 20
for date in tseries['EDM17'].index:
    # find highest price for +1Y with 2 consecutive lows around
    nextExpiryQ = nextExpiryPerMonth[date.month]
    nextExpiryY = date.year -1999 if date.month == 12 else date.year -2000

    baseFutures = ['ED%s%d' % (nextExpiryQ, nextExpiryY)]
    plus1Yspread = []
    plus6Mspread = []
    plus3Mspread = []
    spreadName1Y = []
    spreadName6M = []
    spreadName3M = []
    for x in range(nValues):
        plus1Yfuture = baseFutures[-1][:3] + str(int(baseFutures[-1][3:5])+1)
        plus6Mfuture = baseFutures[-1][:2] + nextQ[nextQ[baseFutures[-1][2]]] + baseFutures[-1][3:5]
        if baseFutures[-1][2] == 'U' or baseFutures[-1][2] == 'Z': plus6Mfuture = baseFutures[-1][:2] + nextQ[nextQ[baseFutures[-1][2]]] + str(int(baseFutures[-1][3:5])+1)
        plus3Mfuture = baseFutures[-1][:2] + nextQ[baseFutures[-1][2]] + baseFutures[-1][3:5]
        if baseFutures[-1][2] == 'Z': plus3Mfuture = baseFutures[-1][:2] + nextQ[baseFutures[-1][2]] + str(int(baseFutures[-1][3:5])+1)

        try:
            plus1Yspread.append( tseries[baseFutures[-1]].ix[date,'Open'] - tseries[plus1Yfuture].ix[date,'Open'])
            spreadName1Y.append(baseFutures[-1] + plus1Yfuture[2:5])
        except KeyError: print 'WARNING: KeyError on', date

        try:
            plus6Mspread.append( tseries[baseFutures[-1]].ix[date,'Open'] - tseries[plus6Mfuture].ix[date,'Open'])
            spreadName6M.append(baseFutures[-1] + plus6Mfuture[2:5])
        except KeyError: print 'WARNING: KeyError on', date

        try:
            plus3Mspread.append( tseries[baseFutures[-1]].ix[date,'Open'] - tseries[plus3Mfuture].ix[date,'Open'])
            spreadName3M.append(baseFutures[-1] + plus3Mfuture[2:5])
        except KeyError: print 'WARNING: KeyError on', date

        # add next base future to list
        if baseFutures[-1][2] == 'Z': baseFutures.append('EDH' + str(int(baseFutures[-1][3:5])+1) )
        else: baseFutures.append( 'ED' + nextQ[baseFutures[-1][2]] + baseFutures[-1][3:5] )

    spreadCurve[date.strftime('%Y-%m-%d')] = (spreadName6M, plus6Mspread)


# spread curves are now in spreadCurve, start analysing
cumulPnLweek = {}
for takeprofit in [0.04, 0.05, 0.06, 0.07]:
    nSumDays = 50
    sumDay = []
    for i in range(nSumDays+1): sumDay.append(0)
    day = ['start']
    cumulPnL = [0]
    week = [0]
    cumulPnLweek[takeprofit] = [0]
    month = [0]
    cumulPnLmonth = [0]
    for date in tseries['EDM17'].index:
        if date.strftime('%Y-%m-%d') in ['2011-12-27','2012-01-05','2012-01-06','2012-01-09','2012-01-11','2012-03-02','2012-03-06','2012-03-09','2012-04-06','2014-02-19','2014-02-27','2014-03-06','2014-03-07']: continue
        
        spreadName = spreadCurve[date.strftime('%Y-%m-%d')][0]
        plusXspread = spreadCurve[date.strftime('%Y-%m-%d')][1]
        idxMax = plusXspread.index( max(plusXspread) )
        if idxMax > len(plusXspread)-4:
            print 'no peak at', date.strftime('%Y-%m-%d')
            continue
        # print date.strftime('%Y-%m-%d'), 'max spread:', spreadName[idxMax], plus1Yspread[idxMax], idxMax
    
        Sm3 = spreadName[idxMax-3]
        Sm2 = spreadName[idxMax-2]
        Sm1 = spreadName[idxMax-1]
        Smax = spreadName[idxMax]
        Sp1 = spreadName[idxMax+1]
        Sp2 = spreadName[idxMax+2]
        Sp3 = spreadName[idxMax+3]
    
        priceSm3 = []
        priceSm2 = []
        priceSm1 = []
        priceSmax = []
        priceSp1 = []
        priceSp2 = []
        priceSp3 = []
        priceCombo = []
        for d in tseries['EDM17'].ix[date:].index[0:nSumDays+1]:
            try:
                priceSm3.append( spreadCurve[d.strftime('%Y-%m-%d')][1][spreadCurve[d.strftime('%Y-%m-%d')][0].index(Sm3)] )
                priceSm2.append( spreadCurve[d.strftime('%Y-%m-%d')][1][spreadCurve[d.strftime('%Y-%m-%d')][0].index(Sm2)] )
                priceSm1.append( spreadCurve[d.strftime('%Y-%m-%d')][1][spreadCurve[d.strftime('%Y-%m-%d')][0].index(Sm1)] )
                priceSmax.append( spreadCurve[d.strftime('%Y-%m-%d')][1][spreadCurve[d.strftime('%Y-%m-%d')][0].index(Smax)] )
                priceSp1.append( spreadCurve[d.strftime('%Y-%m-%d')][1][spreadCurve[d.strftime('%Y-%m-%d')][0].index(Sp1)] )
                priceSp2.append( spreadCurve[d.strftime('%Y-%m-%d')][1][spreadCurve[d.strftime('%Y-%m-%d')][0].index(Sp2)] )
                priceSp3.append( spreadCurve[d.strftime('%Y-%m-%d')][1][spreadCurve[d.strftime('%Y-%m-%d')][0].index(Sp3)] )
    
                diffSm3 = priceSm3[-1] - priceSm3[0]
                diffSm2 = priceSm2[-1] - priceSm2[0]
                diffSm1 = priceSm1[-1] - priceSm1[0]
                diffSmax = priceSmax[-1] - priceSmax[0]
                diffSp1 = priceSp1[-1] - priceSp1[0]
                diffSp2 = priceSp2[-1] - priceSp2[0]
                diffSp3 = priceSp3[-1] - priceSp3[0]
                # priceCombo.append( +diffSm3 +diffSm2 +diffSm1 -(6*diffSmax) +diffSp1 +diffSp2 +diffSp3 )
                priceCombo.append( +diffSm2 -(2*diffSmax) +diffSp2 )
            except ValueError:
                print 'ValueError in', d
                continue
    
        spreadLoss = .0
        for i in range(1,nSumDays+1):
            if len(priceCombo) > i and abs(priceCombo[i])<1: sumDay[i] += (priceCombo[i] - spreadLoss)
        # print date.strftime('%Y-%m-%d'), S1,S2,S3, idxMax
        # print ['%.3f' % p for p in priceCombo]
    
        daysInMarket = 50
        if len(priceCombo) > daysInMarket and abs(priceCombo[daysInMarket])<1:
            day.append(date.strftime('%Y-%m-%d'))
            cumulPnL.append(cumulPnL[-1] + priceCombo[daysInMarket] - spreadLoss)
    
        dow = 4 # monday = 0
        peakIdx = 14
        # takeprofit = .055
        if date.dayofweek == dow and len(priceCombo) > daysInMarket:
            week.append(date.strftime('%Y-%m-%d'))
            for t in range(1,daysInMarket):
                if priceCombo[t] > takeprofit and abs(priceCombo[t])<1: # take profit
                    cumulPnLweek[takeprofit].append(cumulPnLweek[takeprofit][-1] + priceCombo[t] - spreadLoss)
                    break
                if priceCombo[t] < -(takeprofit*10) and abs(priceCombo[t])<1: # stoploss
                    cumulPnLweek[takeprofit].append(cumulPnLweek[takeprofit][-1] + priceCombo[t] - spreadLoss)
                    break
            else:
                if abs(priceCombo[daysInMarket])<1: cumulPnLweek[takeprofit].append(cumulPnLweek[takeprofit][-1] + priceCombo[daysInMarket] - spreadLoss)
                else: cumulPnLweek[takeprofit].append(cumulPnLweek[takeprofit][-1] + priceCombo[daysInMarket-1] - spreadLoss)
    
        daysInMarket = 20
        if date.dayofweek == dow and len(priceCombo) > daysInMarket and abs(priceCombo[daysInMarket])<1:
            month.append(date.strftime('%Y-%m-%d'))
            cumulPnLmonth.append(cumulPnLmonth[-1] + priceCombo[daysInMarket] - spreadLoss)
    
    for j in range(0,nSumDays+1,10): print 'day', j, sumDay[j]

    startIdx = 0
    # plt.plot(range(startIdx,len(cumulPnL)), cumulPnL[startIdx:])
    plt.plot(range(startIdx,len(cumulPnLweek[takeprofit])), cumulPnLweek[takeprofit][startIdx:])
    # plt.xticks(range(startIdx,len(day)), day[startIdx:], rotation='vertical')
plt.legend(['tp = 0.04', 'tp = 0.05', 'tp = 0.06', 'tp = 0.07'], loc='upper left', fancybox=True, shadow=True)
plt.title('Eurodollar cumulative PnL')
plt.xlabel('# trades')
plt.ylabel('ticks x100 (x$2500)')
plt.show()

"""
# plot some as cross check
idxMax = spreadCurve[testDate][1].index( max(spreadCurve[testDate][1]) )
print 'highest price:', spreadCurve[testDate][0][idxMax], spreadCurve[testDate][1][idxMax]

plt.bar(range(nValues), spreadCurve[testDate][1], align='center')
plt.xticks(range(len(spreadCurve[testDate][0])), spreadCurve[testDate][0], rotation='vertical')
plt.title('GE 1Y spreads ' + testDate)
plt.yticks(np.arange(0,1.5,.1))
plt.axes().yaxis.grid(True, 'both')
plt.show()
"""