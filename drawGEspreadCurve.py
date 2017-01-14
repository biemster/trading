#!/usr/bin/env python
# import matplotlib
# matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import numpy as np

""" TWS stuff """
from ib.ext.Contract import Contract
from ib.ext.ContractDetails import ContractDetails
from ib.ext.ComboLeg import ComboLeg
from ib.opt import Connection, message
from time import sleep

# global tws connection
tws_conn = Connection.create(port=7496, clientId=4000)
futures = []
contractDetails = {}
reqIDs = {}
tickSymbols = {}
askPrice = {}
lastPrice = {}
closePrice = {}

def error_handler(msg):
    """Handles the capturing of error messages"""
    print "Server Error: %s" % msg

def reply_handler(msg):
    """Handles of server replies"""
    print "Server Response: %s, %s" % (msg.typeName, msg)

def NextValidIdHandler(msg):
    global nextOrderId
    nextOrderId = msg.orderId

def ContractDetailsHandler(msg):
    contractDetails[msg.reqId] = msg.contractDetails

def LastPriceHandler(msg):
    if msg.field == 9: closePrice[tickSymbols[msg.tickerId]] = float(msg.price)
    if msg.field == 4:
        lastPrice[tickSymbols[msg.tickerId]] = float(msg.price)
        # print 'LAST', tickSymbols[msg.tickerId] + ':', msg.price
        # print len(lastPrice), len(tickSymbols)
        # if len(lastPrice) == len(tickSymbols): drawCurve()
    if msg.field == 2:
        askPrice[tickSymbols[msg.tickerId]] = float(msg.price)
        print 'ASK', tickSymbols[msg.tickerId] + ':', msg.price

def makeFutContract(sym):
    newFutContract = Contract()
    newFutContract.m_localSymbol = sym
    newFutContract.m_secType = 'FUT'
    if sym[:2] == 'GE': newFutContract.m_exchange = 'GLOBEX'
    if sym[:2] == 'ZQ': newFutContract.m_exchange = 'ECBOT'
    newFutContract.m_currency = 'USD'
    return newFutContract

def makeComboLeg(conId, ratio, action):
    newComboLeg = ComboLeg()
    newComboLeg.m_conId = conId
    newComboLeg.m_ratio = ratio
    newComboLeg.m_action = action
    newComboLeg.m_exchange = 'GLOBEX'
    return newComboLeg

def makeBagContract(sym, legs):
    newBagContract = Contract()
    newBagContract.m_symbol = sym
    newBagContract.m_secType = 'BAG'
    newBagContract.m_exchange = 'GLOBEX'
    newBagContract.m_currency = 'USD'
    newBagContract.m_comboLegs = legs
    return newBagContract

def makeSpreadContract(f1,f2):
    leg1 = makeComboLeg(contractDetails[reqIDs[f1]].m_summary.m_conId, 1, 'BUY')
    leg2 = makeComboLeg(contractDetails[reqIDs[f2]].m_summary.m_conId, 1, 'SELL')

    return makeBagContract('GE',[leg1,leg2])

def requestQuotes():
    # make contracts for futures and request contract details
    for f in futures: tws_conn.reqContractDetails(reqIDs[f], makeFutContract(f))
    sleep(3)

    # request quotes for +3M, +6M, +9M and +1Y spreads
    tickId = 1000
    for f in range(len(futures)-4):
        tws_conn.reqMktData(tickId, makeFutContract(futures[f]), '', False)
        tickSymbols[tickId] = futures[f]
        for x in range(1,5):
            tws_conn.reqMktData(tickId+x, makeSpreadContract(futures[f],futures[f+x]), '', False)
            tickSymbols[tickId+x] = futures[f] + futures[f+x][-2:]
        tickId = tickId+5

def drawCurve():
    plt.close()

    pPlotOutrightGE = []
    pPlotYieldGE = []
    pPlot1 = []
    pPlot2 = []
    pPlot3 = []
    pPlot4 = []
    for i in range(len(futures)-4):
        pPlotOutrightGE.append( askPrice.get(futures[i],0) )
        pPlot1.append( askPrice.get(futures[i]+futures[i+1][-2:],0) )
        pPlot2.append( askPrice.get(futures[i]+futures[i+2][-2:],0) )
        pPlot3.append( askPrice.get(futures[i]+futures[i+3][-2:],0) )
        pPlot4.append( askPrice.get(futures[i]+futures[i+4][-2:],0) )

        if i==0: pPlotYieldGE.append( 1 - (askPrice.get(futures[i],0) / 100) )
        else: pPlotYieldGE.append( ((1+pPlotYieldGE[-1])**i * (2-(askPrice.get(futures[i],0)/100)))**(1./(i+1)) -1)

    

    fig,(axOutright,axYield,axSpreads) = plt.subplots(3, sharex=True)
    w = .2
    plus3m = axSpreads.bar(np.arange(len(futures)-4)-2*w, pPlot1, width=w, color='r', align='center')
    plus6m = axSpreads.bar(np.arange(len(futures)-4)-w,   pPlot2, width=w, color='g', align='center')
    plus9m = axSpreads.bar(np.arange(len(futures)-4),     pPlot3, width=w, color='b', align='center')
    plus1y = axSpreads.bar(np.arange(len(futures)-4)+w,   pPlot4, width=w, color='m', align='center')
    lineX = [pPlot1.index(max(pPlot1)), pPlot2.index(max(pPlot2)), pPlot3.index(max(pPlot3)), pPlot4.index(max(pPlot4))]
    lineY = [max(pPlot1), max(pPlot2), max(pPlot3), max(pPlot4)]
    
    axOutright.plot(range(len(futures)-4), pPlotOutrightGE, linestyle='None', marker='h', color='c', markersize=10)
    axOutright.set_yticks(np.arange(97,100,.5))
    axOutright.set_title('eurodollar')
    axYield.plot(range(len(futures)-4), [p*100 for p in pPlotYieldGE], linestyle='None', marker='h', color='c', markersize=10)

    plt.xticks(range(len(futures)-4), futures, rotation='vertical')
    fig.subplots_adjust(hspace=0)
    
    axSpreads.plot(lineX,lineY, color="lime", solid_capstyle='round', solid_joinstyle='round', linewidth=10)
    axSpreads.set_yticks(np.arange(0,0.7,.1))
    axSpreads.legend( (plus3m, plus6m, plus9m, plus1y), ('+3M spreads (H,M)', '+6M spreads (H,U)', '+9M spreads (H,Z)', '+1Y spreads (Hn,Hn+1)') )
    
    axSpreads.grid(True, 'both')
    plt.show(block=False)


if __name__ == "__main__":
    tws_conn.register(error_handler, 'Error')
    tws_conn.register(NextValidIdHandler, 'NextValidId')
    tws_conn.register(ContractDetailsHandler, 'ContractDetails')
    tws_conn.register(LastPriceHandler, message.tickPrice)
    # tws_conn.registerAll(reply_handler)
    tws_conn.connect()
    
    # fill eurodollar futures list
    nextExpiry = 'GEH6'
    nextQ = {'H':'M', 'M':'U', 'U':'Z', 'Z':'H'}
    futures.append(nextExpiry)
    reqIDs[nextExpiry] = 100
    for reqId in range(reqIDs[nextExpiry]+1,reqIDs[nextExpiry]+20):
        if futures[-1][2] == 'Z': futures.append( futures[-1][:2] + nextQ[futures[-1][2]] + str(int(futures[-1][3]) +1) )
        else: futures.append( futures[-1][:2] + nextQ[futures[-1][2]] + futures[-1][3] )

        if len(futures[-1]) == 5: futures[-1] = futures[-1][:3] + futures[-1][-1]
        reqIDs[futures[-1]] = reqId
    
    # request quotes for futures
    requestQuotes()

    inp = ''
    while inp != 'q':
        inp = raw_input('type d+Enter to draw curve, q+Enter to disconnect\n')
        if inp == 'd': drawCurve()
    tws_conn.disconnect()
