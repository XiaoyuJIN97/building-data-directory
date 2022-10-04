# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 09:51:57 2022

@author: patri
"""

import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

st.title('NBA Player Stats Explorer')

st.markdown("""
This app performs simple webscraping of NBA player stats data!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/).
""")

st.sidebar.header('User Input Features')

path_dataset = r'C:\Users\patri\bdg3\dataset'
dataset_info = pd.read_excel(os.path.join(path_dataset, 'Dataset Intro List.xlsx'), header=None)
dataset_info.loc[2, dataset_info.loc[2].isna()] = dataset_info.loc[1, dataset_info.loc[2].isna()]
dataset_info.loc[2, dataset_info.loc[2].isna()] = dataset_info.loc[0, dataset_info.loc[2].isna()]
dataset_info.columns = dataset_info.loc[2]
dataset_info = dataset_info.drop([0,1,2]).reset_index(drop=True)
dataset_info = dataset_info.apply(pd.to_numeric, errors='ignore')
dataset_info.columns = dataset_info.columns.str.replace('\u202f', '')
dataset_info.columns = dataset_info.columns.str.replace('\xa0', '')
dataset_info = dataset_info.iloc[:, :5]

var1 = 'Data Opening Level (requires further discussion)'
# Sidebar - opening level selection
list_var1 = sorted(dataset_info[var1].unique())
selected_var1 = st.sidebar.multiselect(var1, list_var1, list_var1)

var2 = 'Country'
# Sidebar - Country selection
list_var2 = sorted(dataset_info[var2].unique())
selected_var2 = st.sidebar.multiselect(var2, list_var2, list_var2)

# Filtering data
dataset_info_filtered = dataset_info[(dataset_info[var1].isin(selected_var1)) & (dataset_info[var2].isin(selected_var2))]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(dataset_info_filtered.shape[0]) + ' rows and ' + str(dataset_info_filtered.shape[1]) + ' columns.')
st.dataframe(dataset_info_filtered)

