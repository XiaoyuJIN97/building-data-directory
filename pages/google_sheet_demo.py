# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 10:03:01 2022

@author: 靳笑宇
"""

import streamlit as st 
from pandas import DataFrame

from gspread_pandas import Spread,Client
from google.oauth2 import service_account

import ssl 
ssl._create_default_https_context = ssl._create_unverified_context

# Create a Google Authentication connection object
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes = scope)
client = Client(scope=scope,creds=credentials)

spreadsheetname = "Energy Dataset Intro List 1017"
spread = Spread(spreadsheetname,client = client)

# Check the connection
st.write(spread.url)

sh = client.open(spreadsheetname)
worksheet_list = sh.worksheets()

# Functions 
@st.cache(ttl=100)
# Get our worksheet names
def worksheet_names():
    sheet_names = []   
    for sheet in worksheet_list:
        sheet_names.append(sheet.title)  
    return sheet_names

# Get the sheet as dataframe
def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = DataFrame(worksheet.get_all_records())
    return df

# Update to Sheet
def update_the_spreadsheet(spreadsheetname,dataframe):
    col = ['Compound CID','Time_stamp']
    spread.df_to_sheet(dataframe[col],sheet = spreadsheetname,index = False)
    st.sidebar.info('Updated to GoogleSheet')
    
st.header('Building Energy and Water Data')
# Check whether the sheets exists
what_sheets = worksheet_names()
#st.sidebar.write(what_sheets)
ws_choice = st.sidebar.radio('Available worksheets',what_sheets)
# Load data from worksheets
df = load_the_spreadsheet(ws_choice)
# Show the availibility as selection
select_CID = st.sidebar.selectbox('Name',list(df['Dataset Full Name']))

