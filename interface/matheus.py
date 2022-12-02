
# Importing Libraries

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from prophet import Prophet
import os

# Loading Datasets

path = "/home/thomas-ff/code/project_lewagon/blast-from-the-forecast/raw_data/"
os.path.join(path, "item_categories.csv")

sales_df = pd.read_csv(os.path.join(path, "sales_train.csv"))

# Variables
Month = sales_df['date_block_num']
Count = sales_df['item_cnt_day']
Shop = sales_df['shop_id']
Price = sales_df['item_price']

# Creating the pages

st.sidebar.title('Tool of Thumb')
selectedpage = st.sidebar.selectbox('Select the page',['Overview', 'Forecast'])

if selectedpage == 'Overview':
    st.title('Overview')
    st.markdown(' ## First glimpse of the dataset')
    st.markdown(" The dataset contains almost 3 millon registers of Video Game related sales, from January/2013 to October/2015. It has 59 different shops, 84 item categories and over 22 thousand items.")
    st.selectbox('Choose a category',['All','0', '1', '2'])
    st.selectbox('Choose a Month/Year',['All','January/2013','February/2013'])
    st.selectbox('Choose a Shop ID',['All','0','1','2'])
    plt.figure(figsize=(10,5))
    sns.lineplot(data=sales_df, x=Month, y=Count, color="blue")
    plt.title('Sales Count per Month')
    plt.xlabel('Month')
    plt.ylabel('Sales Count')
    st.pyplot(plt)
    plt.figure(figsize=(10,5))
    sns.lineplot(data=sales_df, x=Month, y=Price, color="blue")
    plt.title('Sales Revenue per Month')
    plt.xlabel('Month')
    plt.ylabel('Sales Revenue')
    st.pyplot(plt)
    plt.figure(figsize=(15,5))
    sns.barplot(data=sales_df, x=Shop, y=Count, color="blue")
    plt.title('Sales Count per Shop')
    plt.xlabel('Shop ID')
    plt.ylabel('Sales Count')
    st.pyplot(plt)
    plt.figure(figsize=(15,5))
    sns.barplot(data=sales_df, x=Shop, y=Price, color="blue")
    plt.title('Sales Revenue per Shop')
    plt.xlabel('Shop ID')
    plt.ylabel('Sales Revenue')
    st.pyplot(plt)
    plt.clf

elif selectedpage == 'Prediction':
    st.title('Prediction')
    st.selectbox('Choose a category',['All','0', '1', '2'])
    st.selectbox('Choose a Month/Year',['All','January/2013','February/2013'])
    st.selectbox('Choose a Shop ID',['All','0','1','2'])
