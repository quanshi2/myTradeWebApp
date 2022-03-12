# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 19:49:22 2022

@author: Mike Shi
"""
from pandas_datareader import data as pdr
from datetime import date
import datetime as dt
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
import talib
today = date.today()
stockname = "QQQ"

class strategy():
    stk = yf.Ticker(stockname)
    def __init__(self,stockname) :
        self._stockname = stockname
        
    def monthV(self,stk):
        stkData = stk.history(interval = "1mo",start='2010-02-01', end=today)
        mystock_data_month = self.TechAnalysis(stkData)
        return mystock_data_month
    def weekV(self,stk):
        stkData = stk.history(interval = "1wk",start='2020-02-01', end=today)
        mystock_data_week = self.TechAnalysis(stkData)
        return mystock_data_week
    def dayV(self,stk):
        stkData = stk.history(interval = "1d",start='2021-01-01', end=today)
        mystock_data_day = strategy.TechAnalysis(stkData)
        return mystock_data_day
    def hourV(self,stk):
        stkData = stk.history(interval = "1h",start=today - dt.timedelta(days = 7), end=today)
        mystock_data_hour = strategy.TechAnalysis(stkData)
        return mystock_data_hour
    def TechAnalysis(self,stkData):
        stkData_DF = pd.DataFrame.from_dict(stkData)
        # clean empty data
        nan_value = float("NaN")
        stkData_DF.replace("", nan_value, inplace=True)
        stkData_DF.dropna(subset = ["Close"], inplace=True)
        stkDataDF_final = stkData_DF
    
        mystock = stkDataDF_final[['Open', 'High', 'Low', 'Close', 'Volume']]
        close = mystock['Close']
        high = mystock['High']
        low = mystock['Low']
    
        # KDJ parameter
        KDJ_1=9
        KDJ_2=3
        KDJ_3=3
    
        rsi = talib.RSI(close, timeperiod=14)
        rsi.name = 'RSI'
        mystock = pd.concat([mystock, rsi], axis = 1 )
    
        sma = talib.SMA(mystock['Close'],14)
        sma.name = 'SMA'
        mystock = pd.concat([mystock, sma], axis = 1 )
    
        macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
        macd.name = 'Macd'
        macdsignal.name = 'Macd_signal'
        macdhist.name ='Macd_hist'
        mystock = pd.concat([mystock, macd], axis = 1 )
        mystock = pd.concat([mystock, macdsignal], axis = 1 )
        mystock = pd.concat([mystock, macdhist], axis = 1 )
    
        slowK, slowD = talib.STOCH(high, low, close, fastk_period = KDJ_1, slowk_period=KDJ_2, slowk_matype=0, slowd_period=KDJ_3, slowd_matype=0)
        slowK.name = 'K'
        slowD.name = 'D'
        mystock = pd.concat([mystock, slowK, slowD], axis = 1 )
        return mystock

if __name__ == "__main__":
    pass
    

    
