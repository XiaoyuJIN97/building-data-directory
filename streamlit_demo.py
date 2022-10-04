# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 13:00:56 2022

@author: patri
"""

import yfinance as yf
import streamlit as st
import pandas as pd

st.write("""
### Simple Stock price App

Shown are the **stock** closing price and volume of Google!

""")

tickerSymbol = 'GOOGL'

tickerData = yf.Ticker(tickerSymbol)

tickerDf = tickerData.history(period='1d',
                              start='2010-05-31',
                              end='2020-05-31')

st.line_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume)
