# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

"""
Database Loading
"""


import os
os.chdir(r"C:\Users\colli\OneDrive\Documents\Stock Market Project")
import pandas as pd
import time
import numpy as np
from datetime import timedelta, date

#Federal Reserve Data
#Timeframe: Monthly 01/01/1980 to 12/31/2022
df_FedFund = pd.read_csv(r'C:\Users\colli\OneDrive\Documents\Stock Market Project\FEDFUNDS.csv')
print(df_FedFund)

#Put To Call Ratio Data
#TimeFrame: Daily 11/1/2006 to 10/04/2019
df_PutCall = pd.read_csv(r'C:\Users\colli\OneDrive\Documents\Stock Market Project\totalpc.csv')
print(df_PutCall)

#Vix Data 
#Timeframe: Daily Data 01/02/1990 to 01/26/2023
df_Vixcurrent = pd.read_csv(r'C:\Users\colli\OneDrive\Documents\Stock Market Project\VIX_History1990toCurrent.csv')
print(df_Vixcurrent)

#Get only needed columns from vix
df_Vixcurrent = df_Vixcurrent.rename(columns={'DATE': 'VIXDate', 'CLOSE': 'VIXClose'})
print(df_Vixcurrent)
df_Vixcurrent = df_Vixcurrent.drop(['OPEN','HIGH','LOW'], axis=1)

#S&P 500 Data
#TimeFrame: Weekly 01/06/1980 to 01/01/2023
df_SP500 = pd.read_csv(r'C:\Users\colli\OneDrive\Documents\Stock Market Project\^spx_w.csv')
print(df_SP500)

#Consumer Sentiment Data
#Timeframe: Weekly 06/26/1987
df_Sentiment = pd.read_excel(r'C:\Users\colli\OneDrive\Documents\Stock Market Project\sentiment-Edited.xlsx')
print(df_Sentiment)

"""
Final Database Building
"""

#Keeping only necessary columns from S&P data
FinalDB = df_SP500[['Date','Close','Volume']]
print(FinalDB)
#Keeping only necessary rows from S&P data
FinalDB = FinalDB[FinalDB.Date.between('1990-01-01', '2022-12-31')]

#Checking datatypes for join & converting dates to date data type
FinalDB.dtypes
df_Vixcurrent.dtypes
FinalDB['Date'] = pd.to_datetime(FinalDB['Date'])
df_Vixcurrent['VIXDate'] = pd.to_datetime(df_Vixcurrent['VIXDate'])
#adding two days to match data to have sundays value to join with S&P which only has Sundays
df_Vixcurrent['VIXDate'] = df_Vixcurrent['VIXDate'] + timedelta(days=2)


#Joining DB's
FinalDB2 = pd.merge(FinalDB,df_Vixcurrent,left_on='Date',right_on='VIXDate')
print(FinalDB2)

#Getting Year and month column to use to join to Fedrate monthly data
DF_Year_Month = {'Year':[],'Month': []}
DF_Year_Month = pd.DataFrame(DF_Year_Month)
print(DF_Year_Month)
FinalDB2 = FinalDB2.append(DF_Year_Month)
FinalDB2['Year'] = pd.DatetimeIndex(FinalDB2['Date']).year
FinalDB2['Month'] = pd.DatetimeIndex(FinalDB2['Date']).month
FinalDB2["YearMonth"] = FinalDB2['Year'].astype(str) +"-"+ FinalDB2["Month"].astype(str)

#Adding month and year column to fedFund to use for join
df_FedFund = df_FedFund.append(DF_Year_Month)
df_FedFund['Year'] = pd.DatetimeIndex(df_FedFund['DATE']).year
df_FedFund['Month'] = pd.DatetimeIndex(df_FedFund['DATE']).month
df_FedFund["YearMonth"] = df_FedFund['Year'].astype(str) +"-"+ df_FedFund["Month"].astype(str)
df_FedFund = df_FedFund[['FEDFUNDS', 'YearMonth']]

#Join FedFund to finalDB
FinalDB3 = pd.merge(FinalDB2,df_FedFund,on='YearMonth')
print(FinalDB3)

#Drop unnecessary columns
FinalDB3 = FinalDB3.drop(['Year','Month','YearMonth','VIXDate'], axis=1)
FinalDB3 = FinalDB3.rename(columns = {'Close':'SP500_Price'})

#Join Consumer Sentiment to Final DB
df_Sentiment = df_Sentiment.rename(columns = {'Reported Date':'Date'})
df_Sentiment = df_Sentiment[df_Sentiment.Date.between('1990-01-01', '2022-12-31')]
df_Sentiment['Date'] = df_Sentiment['Date'] + timedelta(days=2)
FinalDB4 = pd.merge(FinalDB3,df_Sentiment,on='Date')
FinalDB4.tail(50)


"""
EDA
"""

#Vix value higher than 60 should indicate a market bottom
FinalDB3.loc[FinalDB3['VIXClose'] > 60]
