# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 22:03:34 2022

@author: Yun An Shi
"""

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
# import sys
# sys.path.append('C:/Users/HP/Documents/GitHub/myTradeWebApp')
import imp
from PIL import Image



tradeStrategy = imp.load_source('tradeStrategy', 'C:/Users/HP/Documents/GitHub/myTradeWebApp/tradeStrategy.py')
import tradeStrategy as stgy


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
# stockname = "QQQ"


def web_plot(StockTestName):
    st.title('''Quan's Trading Platform''')
    # Create a table
    st.write("Here's our first attempt at using data to create a table:")
    # st.write(pd.DataFrame({
    #     'first column': [1, 2, 3, 4],
    #     'second column': [10, 20, 30, 40]
    # }))
    
    # draw table
    # st.write(showDataTable.head())
    
    # draw chart
    chart_data = pd.DataFrame(
         np.random.randn(20, 3),
         columns=['a', 'b', 'c'])
    
    st.line_chart(chart_data)
    imgFolder = "C:/Users/HP/Documents/GitHub/myTradeWebApp/"
    image = Image.open(imgFolder + 'VC.png')
    st.image(image, caption='stock chart')
    # Widgets， slider
    x = st.slider('x')  # 👈 this is a widget
    st.write(x, 'squared is', x * x)
    
    if st.checkbox('Show dataframe'):
        chart_data = pd.DataFrame(
           np.random.randn(20, 3),
           columns=['a', 'b', 'c'])
        chart_data
    
    option = st.selectbox('Which number do you like best?',chart_data['a'])
    'You selected: ', option

    # Add a slider to the sidebar:
    selectbox_longTimeRange = st.sidebar.selectbox('What Time-Range would you like to run?', \
                                          ('One week', 'One hour', 'One day'))
    'Time range: ', selectbox_longTimeRange
    if selectbox_longTimeRange == 'One week': 
        interval_str = "1wk"
    elif selectbox_longTimeRange == 'One hour': 
        interval_str = "1h"
    elif selectbox_longTimeRange == 'One day':
        interval_str = "1d"
    else:
        st.write('something wrong, pls check!')
    # # Add a slider to the sidebar:
    # selectbox_shortTimeRange = st.sidebar.selectbox('What Time-Range would you like to run?', \
    #                                       ('One hour', 'Five minutes', 'One day'))
    # 'Time range: ', selectbox_shortTimeRange
    

    add_slider = st.sidebar.slider(
        'Select stock price range',
        0, 700, (50, 280))
    
    col_name = ()
    loadResult  = pd.read_csv('C:/Users/HP/Documents/GitHub/myTradeWebApp/myPickStock.csv')
    records = loadResult.to_records(index = False)
    index, col_name, col_date, col_price = zip(*records) 
    # Selectbox_findStockName = st.sidebar.selectbox('List of detected stock',col_name)
    if st.sidebar.button('Start Searching Stock'):
        myStockToCheck = TechAnalysis(StockTestName, selectbox_longTimeRange)
        records = myStockToCheck.to_records(index = False)
        col_name, col_date, col_price = zip(*records)      
        if len(col_name) > 1:
            st.write(f'number of stock found is: {col_name}')    
        else:
            st.write(f'sorry, did not catch anything, number of stock is {col_name}')
    Selectbox_findStockName = st.sidebar.selectbox('List of detected stock',col_name)
    'Check details', Selectbox_findStockName
    
    # use checkbox to display 
    if st.sidebar.checkbox('Show stock picture and closing price'):
        stk = yf.Ticker(str(Selectbox_findStockName))
        
        # stk.info
        stkData = stk.history(interval = interval_str, start='2018-10-01', end=today)
        stkData_DF = pd.DataFrame.from_dict(stkData)
        # clean empty data
        nan_value = float("NaN")
        stkData_DF.replace("", nan_value, inplace=True)
        stkData_DF.dropna(subset = ["Close"], inplace=True)
        stkDataDF_final = stkData_DF
        
        mystock = stkDataDF_final[['Open', 'High', 'Low', 'Close', 'Volume']]
        st.sidebar.chart_data = mystock.iloc[-18:]
        # st.sidebar.chart_data = pd.DataFrame(
        #    np.random.randn(3, 3),
        #    columns=['a', 'b', 'd'])
        st.sidebar.chart_data
        
    
def monthV(stk):
    stkData = stk.history(interval = "1mo",start='2010-02-01', end=today)
    mystock_data_month = TechAnalysis(stkData)
    return mystock_data_month
def weekV(stk):
    stkData = stk.history(interval = "1wk",start='2020-02-01', end=today)
    mystock_data_week = TechAnalysis(stkData)
    return mystock_data_week
def dayV(stk):
    stkData = stk.history(interval = "1d",start='2021-01-01', end=today)
    mystock_data_day = TechAnalysis(stkData)
    return mystock_data_day
def hourV(stk):
    stkData = stk.history(interval = "1h",start=today - dt.timedelta(days = 7), end=today)
    mystock_data_hour = TechAnalysis(stkData)
    return mystock_data_hour
def plotBarchart():
    padnum = 30
    apds = [ mpf.make_addplot(slowK[padnum:], panel=1,color='r',type='line',secondary_y=True, linestyle='dotted'),
            mpf.make_addplot(slowD[padnum:], panel=1,color='b',type='line',secondary_y=True, linestyle='dotted'),

            mpf.make_addplot(macd[padnum:], panel=2,color='r',type='line',secondary_y=True, width=0.5),
            mpf.make_addplot(macdsignal[padnum:], panel=2,color='b',type='line',secondary_y=True, width=1),
            mpf.make_addplot(macdhist[padnum:],panel=2,color='g',type='bar', width=0.75,secondary_y=True)
           ]

    # 价格:panel = 0,
    # KDJ 和成交量 ：panel = 1
    # MACD : panel = 2

    mpf.plot(mystock[padnum:],type='candle', style='charles',
                title= 'Stock -' + '"'+stockname +'"' + ' weekly analysis',
                ylabel='Price ($)',
                ylabel_lower='Shares \nTraded',
                volume=True, 
                mav=(5,10,20),
                addplot=apds,
                figscale=1.6,
                savefig= './up_week_image/' + stockname + '.png')
    mpf.plot(mystock[padnum:],type='candle', style='charles',
                title= 'Stock -' + '"'+stockname +'"' + ' weekly analysis',
                ylabel='Price ($)',
                ylabel_lower='Shares \nTraded',
                volume=True, 
                mav=(5,10,20),
                addplot=apds,
                figscale=1.6)
def TechAnalysis(StockTestName, period):
    if period == 'One week': 
        interval_str = "1wk"
    elif period == 'One hour': 
        interval_str = "1h"
    elif period == 'One day':
        interval_str = "1d"
    else:
        st.write('something wrong, pls check!')
    
    myPickStockUp = pd.DataFrame(columns=['stockID','Date','Close'])
    # for  ind in StockTestName.index:
    for  ind in range(100):
        stockname = StockTestName['name'][ind]
    #     print(StockTestName['name'][ind])
        stk = yf.Ticker(stockname)
        
        # stk.info
        stkData = stk.history(interval = interval_str, start='2018-10-01', end=today)
        if len(stkData) > 52: # must have at least 52 weeks data
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
            if ((mystock['Macd_hist'].iloc[-1] - mystock['Macd_hist'].iloc[-2]) > 0 and (mystock['Macd_hist'].iloc[-3] - mystock['Macd_hist'].iloc[-2])) > 0:
            #  cond 1: it is a turning point，拐点出现
                # if mystock['Macd_hist'].iloc[-3] < mystock['Macd_hist'].iloc[-4] and mystock['Macd_hist'].iloc[-4] < mystock['Macd_hist'].iloc[-5]:
                #     # cond 2: last three days 回调中
                    
                #     trend_MACD = mystock['Macd_signal'].diff()
                #     if trend_MACD.iloc[-5] > 0 and trend_MACD.iloc[-4] > 0 and trend_MACD.iloc[-3] > 0 and trend_MACD.iloc[-2] > 0 and trend_MACD.iloc[-1] > 0:
                #         # cond 3: macdsignal(DEA) 主趋势向上 (trend_MACD)
                new_row = {'stockID':stockname, 'Date':today, 'Close':close.iloc[-1]}
                myPickStockUp = myPickStockUp.append(new_row, ignore_index=True)
                myPickStockUp.to_csv('C:/Users/HP/Documents/GitHub/myTradeWebApp/myPickStock_' + str(today) + '.csv')
    return myPickStockUp

if __name__ == '__main__':
    # stgy_perc_5 = stgy.strategy()
    # stgy_perc_10 = stgy.strategy()
    # stgy_perc_30 = stgy.strategy()
    StockTestName = pd.read_csv('C:/Users/HP/Documents/GitHub/myTradeWebApp/stock_Price5_Volume100k.csv')
    
    web_plot(StockTestName)
    # stockname = "QQQ"
    # stk = yf.Ticker(stockname)
    # weekDataTable = weekV(stk)
    # showDataTable = weekDataTable
    # print(showDataTable.head())
    # web_plot(showDataTable)


