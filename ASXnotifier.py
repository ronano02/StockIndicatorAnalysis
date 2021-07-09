import yfinance as yf
import pandas as pd
import numpy as np
import time

stockTickers = ['AGL.AX', 'ANZ.AX', 'APT.AX', 'CAR.AX', 'COL.AX', 'DMP.AX', 'JBH.AX', 'QAN.AX', 'SUN.AX', 'TLS.AX']


def indicatorMACD(data):
    exp1 = data['Close'].ewm(span=12, adjust=False).mean()
    exp2 = data['Close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signalLine = macd.ewm(span=9, adjust=False).mean()
    return [macd, signalLine]


def indicatorRSI(data):
    change = data['Close'].diff(1)
    up = change.mask(change < 0, 0)
    down = change.mask(change > 0, 0)
    avgUp = up.ewm(com=13, adjust=False).mean()
    avgDown = down.ewm(com=13, adjust=False).mean()
    rs = abs(avgUp / avgDown)
    rsi = 100 - (100 / (1 + rs))
    return rsi


def buyOrSell(macddata, signaldata, rsidata):
    buy, sell = 0, 0
    if macddata[-1] > signaldata[-1] and (macddata[-2] < signaldata[-2] or macddata[-2] == signaldata[-2]): buy += 1
    elif macddata[-1] < signaldata[-1] and (macddata[-2] > signaldata[-2] or macddata[-2] == signaldata[-2]): sell += 1

    if rsidata[-1] < 35: buy += 1
    elif rsidata[-1] > 65: sell += 1

    if buy == 2: return "Strong indication to buy the stock"
    elif sell == 2: return "Strong indication to sell the stock"
    else: return "No strong indication to buy or sell"


# Refreshes every 2 minutes, recalculating each stock's RSI and MACD values.
# Prints time, stock ticker, MACD/RSI values, and if there is any strong indication to buy/sell
while True:
    for stock in stockTickers:
        stockData = yf.download(tickers=stock, period='1mo', interval='2m', auto_adjust=True)
        print('\n' + stock + '\n')

        dateTime = str(stockData.index[-1]).split('-')
        day = dateTime[1]
        monthAndTime = dateTime[2].split(' ')
        print(day + f'/{monthAndTime[0]}  {monthAndTime[1]}')

        macdValues = indicatorMACD(stockData)
        rsiValues = indicatorRSI(stockData)
        print(f'MACD equals: {round(macdValues[0][-1], 4)}')
        print(f'Signal Line equals: {round(macdValues[1][-1], 4)}')
        print(f'RSI equals: {round(rsiValues[-1], 2)} \n')
        print(buyOrSell(macdValues[0], macdValues[1], rsiValues))
        print('')

    time.sleep(120)

# When macd > signal it is a bullish market
# When macd < signal it is a bearish market
# When rsi > 70 it is overbought
# When rsi < 30 it is oversold
