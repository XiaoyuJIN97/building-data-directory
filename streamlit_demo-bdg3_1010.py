# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 09:43:54 2022

@author: 靳笑宇
"""

import streamlit as st
import pandas as pd
import base64
import numpy as np
import altair as alt

st.title('High-level List Visualization')

st.markdown("""
This app performs simple visualization of the high-level list.
* **Python libraries:** base64, pandas, streamlit
""")

st.sidebar.header('User Input Features')

#path_dataset = r'C:\Users\靳笑宇\Desktop\projects in NUS\Building Directory\Dataset intro\visualization\streamlit\dataset'
dataset = pd.read_excel('https://github.com/XiaoyuJIN97/building-data-directory/blob/master/Dataset%20Intro%20List%201010.xlsx?raw=true', header=None)
#%%
#向下填充column name使得line 2 的column name皆为有效
dataset.loc[2, dataset.loc[2].isna()] = dataset.loc[1, dataset.loc[2].isna()]
dataset.loc[2, dataset.loc[2].isna()] = dataset.loc[0, dataset.loc[2].isna()]
#%%
dataset.columns = dataset.loc[2]
dataset = dataset.drop([0,1,2]).reset_index(drop=True)
dataset = dataset.apply(pd.to_numeric, errors='ignore')
dataset.columns = dataset.columns.str.replace('\u202f', '')
dataset.columns = dataset.columns.str.replace('\xa0', '')
dataset.columns = dataset.columns.str.replace('55154\\u202f', '')
dataset.columns = dataset.columns.str.replace('\u202f\xa0', '')
#dataset_info = [str(x).encode('UTF8') for x in dataset_info]
#%%
dataset_info = dataset.iloc[:35, :8]
dataset_info ['Building Type'] = dataset['Building Type']
dataset_info ['URL'] = dataset['URL']
dataset_info.iloc[:,:9] = dataset_info.iloc[:,:9].astype(str)

dataset_info ['Start Year of Recording'] = dataset['Starting Year of Recording']
dataset_info ['End Year of Recording'] = dataset['End Year of Recording (by 06/09/2022)']

dataset_info ['Earliest Year of Built'] = dataset['Earliest Year of Built']
dataset_info ['Latest Year of Built'] = dataset['Latest Year of Built']

dataset_info ['Minimum Floor Area'] = dataset['Minimum Floor Area (m2)']
dataset_info ['Maximum Floor Area'] = dataset['Maximum Floor Area (m2)']

dataset_info['Sample Number'] = dataset['Sample Number'] 
dataset_info['Variable Number'] = dataset['Variable Number']
#%%
country_list = dataset_info['Country'].unique().tolist()
country_list.append('All')
country_list.sort()
selected_country = st.sidebar.selectbox('Country', country_list)
if selected_country!= 'All':
    dataset_info = dataset_info.loc[dataset_info['Country']==selected_country]
else:
    dataset_info = dataset_info

city_list = dataset_info['City/District'].unique().tolist()
city_list.append('All')
city_list.sort()
selected_city = st.sidebar.selectbox('City/District', city_list)
if selected_city!= 'All':
    dataset_info = dataset_info.loc[dataset_info['City/District']==selected_city]
else:
    dataset_info = dataset_info
#%%
var1 = 'Time Interval'
list_var1 = sorted(dataset_info[var1].unique())
selected_var1 = st.sidebar.multiselect(var1, list_var1, list_var1)

#%%
var2 = 'Building Type'
# Sidebar - Building type selection
list_var2 = sorted(dataset_info[var2].unique())
selected_var2 = st.sidebar.multiselect(var2, list_var2, list_var2)

#%%
# Filtering data
dataset_info_filtered = dataset_info[(dataset_info[var1].isin(selected_var1)) & (dataset_info[var2].isin(selected_var2))]

st.write('Data Dimension: ' + str(dataset_info_filtered.shape[0]) + ' rows and ' + str(dataset_info_filtered.shape[1]) + ' columns.')

#%%
def filedownload(df):
   csv = df.to_csv(index=False)
   b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
   href = f'<a href="data:file/csv;base64,{b64}" download="dataset_info.csv">Download CSV File</a>'
   return href
#%%
dataset_info_filtered.reset_index(drop = True, inplace = True)
#%%
for i in range(len(dataset_info_filtered)):
    url = dataset_info_filtered['URL'][i]
    dataset_info_filtered['URL'][i] =  f'<a href="{url}">{url}</a>'
#%%
dataset_info_filtered = dataset_info_filtered.reset_index(drop=True)
dataset_html = dataset_info_filtered.to_html(escape=False)
st.write(dataset_html, unsafe_allow_html=True)
#st.dataframe(dataset_info_filtered)
st.markdown(filedownload(dataset_info_filtered), unsafe_allow_html=True)
#%%
#Bar plot for recording year
with st.expander("Recording Years"):
    st.markdown("""
    * **Recording Years**
    """)
    y_axis1 = alt.Axis(
        offset=5,
        #labelLimit=500,
        #minExtent=200,
        domain=False
    )
    
    bar1 = alt.Chart(dataset_info_filtered).mark_bar().encode(
        x=alt.X('Start Year of Recording', scale=alt.Scale(domain=[1978, 2023])),
        x2='End Year of Recording',
        y=alt.Y('Dataset Abbreviation', title="Datasets", axis=y_axis1)
    ).properties(
        width=450,
        height=500
    ).configure_axisY(
        titleAngle=0,
        titleY=-10,
        titleX=-10,
    )
    st.altair_chart(bar1.interactive(), use_container_width=True)
#%%
#Bar plot for year of built
with st.expander("Year of Built"):
    st.markdown("""
    * **Year of Built**
    """)
    y_axis2 = alt.Axis(
        offset=5,
        domain=False
    )
    bar2 = alt.Chart(dataset_info_filtered).mark_bar().encode(
        x=alt.X('Earliest Year of Built', scale=alt.Scale(domain=[1900, 2023])),
        x2='Latest Year of Built',
        y=alt.Y('Dataset Abbreviation', title="Datasets", axis=y_axis2)
    ).properties(
        width=450,
        height=500
    ).configure_axisY(
        titleAngle=0,
        titleY=-10,
        titleX=-10,
    )
    st.altair_chart(bar2.interactive(), use_container_width=True)
#%%
#Bar plot for floor area
with st.expander("Floor Areas"):
    st.markdown("""
    * **Floor Areas (square meter)**
    """)
    
    y_axis3 = alt.Axis(
        offset=5,
        domain=False
    )
    bar3 = alt.Chart(dataset_info_filtered).mark_bar().encode(
        x=alt.X('Minimum Floor Area', scale=alt.Scale(domain=[0, 1000000])),
        x2='Maximum Floor Area',
        y=alt.Y('Dataset Abbreviation', title="Datasets", axis=y_axis3)
    ).properties(
        width=450,
        height=500
    ).configure_axisY(
        titleAngle=0,
        titleY=-10,
        titleX=-10,
    )
    st.altair_chart(bar3.interactive(), use_container_width=True)    
#%%
#Bubble plot for sample number
with st.expander("Sample Numbers"):
    st.markdown("""
    * **Sample Numbers**
    """)
    
    bub1 = alt.Chart(dataset_info_filtered).mark_circle().encode(
        alt.X('Sample Number', scale=alt.Scale(zero=False)),
        alt.Y('Dataset Abbreviation', title="Datasets",scale=alt.Scale(zero=False, padding=1)),
        #color='Dataset Abbreviation',
        size='Sample Number'
    ).properties(
        width=600,
        height=450
    ).configure_axisY(
        titleAngle=0,
        titleY=-10,
        titleX=-10,
    )
    st.altair_chart(bub1.interactive(), use_container_width=True)   
#%%
#Bubble plot for variable number
with st.expander("Variable Numbers"):
    st.markdown("""
    * **Variable Numbers**
    """)
    
    bub1 = alt.Chart(dataset_info_filtered).mark_circle().encode(
        alt.X('Variable Number', scale=alt.Scale(zero=False)),
        alt.Y('Dataset Abbreviation', title="Datasets",scale=alt.Scale(zero=False, padding=1)),
        #color='Dataset Abbreviation',
        size='Variable Number'
    ).properties(
        width=600,
        height=450
    ).configure_axisY(
        titleAngle=0,
        titleY=-10,
        titleX=-10,
    )
    st.altair_chart(bub1.interactive(), use_container_width=True)   