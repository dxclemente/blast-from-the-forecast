
import streamlit as st
import os
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
sns.set()

from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
from prophet.plot import plot_cross_validation_metric
from prophet.serialize import model_to_json, model_from_json

import requests
import datetime as dt
from datetime import datetime, timedelta

from load_func import load_sales_df, load_cross_val, load_cv_results, load_model
from load_func import load_final_csv

from models.params import VERSION, STREAMLIT_PATH, CV_PATH, MOODELS_PATH
from models.dict_vars import FEATURE_DICT, F_STREAM_DICT, DF_DICT, PERIOD_DICT, PROPH

#st.set_page_config(layout='wide')
st.set_page_config(
    page_title="Le Wagon Project",
    page_icon="🐍",
    layout="centered",
    initial_sidebar_state="auto"
    )

st.sidebar.title("Blast from the Forecast")
pages = ["Overview", "Validation", "Forecast", "Predict"]
selected_page = st.sidebar.selectbox("Select the page", pages, index=0)

################
### SIDE BAR ###
################

### Overview ###
if selected_page == "Overview":
    col1, col2 = st.sidebar.columns(2)
    with col1:
        df_id = st.radio("Choose a Data Frame:", [
            "Total", "Shop", "Categorie", "Item", "Categorie per Shop"
            ])
    with col2:
        feature = st.radio("Choose a feature:", ["Item Count", "Total Value"])
        period = st.radio("Choose a period:", ["Day", "Week", "Month"])

    version = st.sidebar.text_input(
        "Choese a version", VERSION)

    file_name = "_".join([
        DF_DICT[df_id], F_STREAM_DICT[feature], PERIOD_DICT[period], f"{version}.csv"])
    st.sidebar.write("File Name:", file_name)

### Validation ###
elif selected_page == "Validation":
    feature_total = st.sidebar.radio("Choose a feature:", ["Item Count", "Total Value"])

### Forecast ###
elif selected_page == "Forecast":
    col3, col4 = st.sidebar.columns(2)
    with col3:
        df_id_by = st.radio("Choose a Data Frame:", ["Shop", "Categorie"])
    with col4:
        feat_by = st.radio("Choose a feature:", ["Item Count", "Total Value"])

    ver_by = st.sidebar.text_input(
        "Choese a version", VERSION) # Not used

    model_name = "_".join([
        'prophet', PROPH[df_id_by], "id", PROPH[feat_by]])
    st.sidebar.write("Model Name:", model_name)

### Predict ###
elif selected_page == "Predict":
    st.sidebar.write("Rien ne suffit")

################
### MAIN APP ###
###############$

### Overview ###
if selected_page == "Overview":
    """# Preliminary view of the Data Set"""
    df = load_sales_df(DF_DICT[df_id],
        F_STREAM_DICT[feature],
        PERIOD_DICT[period],
        version,
        path=STREAMLIT_PATH)

    """## Plot Time Series"""
    if DF_DICT[df_id] == "total":
        st.line_chart(df)
    else:
        columns = st.columns(3)
        chosen_id_0 = columns[0].selectbox(f"Choose a {DF_DICT[df_id]} id:", df.columns[1:], key=0)
        chosen_id_1 = columns[1].selectbox(f"Choose a {DF_DICT[df_id]} id:", df.columns[1:], key=1)
        chosen_id_2 = columns[2].selectbox(f"Choose a {DF_DICT[df_id]} id:", df.columns[1:], key=2)
        st.line_chart(df[[chosen_id_0, chosen_id_1, chosen_id_2]])


    """## Plot Distribution Chart"""
    start = st.slider("Selcet Window", 0, df.shape[1]-40)
    df_sum = df.sum().sort_values(ascending=False).iloc[start:50+start]
    fig = plt.figure(figsize=(12, 5))
    bar = sns.barplot(x=df_sum.index, y=df_sum.values, order=df_sum.index)
    plt.tick_params(axis='x', labelsize=10, rotation=90)
    plt.tick_params(axis='y', labelsize=10)
    st.pyplot(fig)

### Validation ###
elif selected_page == "Validation":
    """# Validation"""
    model = load_cross_val(CV_PATH, F_STREAM_DICT[feature_total], 'model', '.gz')
    forecast = load_cross_val(CV_PATH, F_STREAM_DICT[feature_total], 'forecast', '.csv')
    train = load_cross_val(CV_PATH, F_STREAM_DICT[feature_total], 'train', '.csv')
    test = load_cross_val(CV_PATH, F_STREAM_DICT[feature_total], 'test', '.csv')
    horizon = load_cross_val(CV_PATH, F_STREAM_DICT[feature_total], 'horizon', '.pkl')

    """## Prophet Model"""
    with st.expander("Show Model:"):
        st.write(model.plot(forecast))

    """## Test, Train and Forecast Data"""
    with st.expander("Show Plots:"):
        fig1, ax1 = plt.subplots(figsize=(12, 6))
        plt.plot(train['ds'], train['y'], label="Train")
        plt.plot(test['ds'], test['y'], label="Train")
        plt.plot(forecast['ds'][930:], forecast['yhat'][930:], label="Train")
        plt.tick_params(axis='x', labelsize=12, rotation=45)
        plt.tick_params(axis='y', labelsize=12)

        # SLIDER to chage the plot
        start = st.slider("Selcet Range:", 0, 36, 0)
        start_tick = dt.datetime.strptime('2013-01', '%Y-%m').date()
        delta_tick = start*timedelta(days=28)
        right_tick = dt.datetime.strptime('2016-01', '%Y-%m').date()

        plt.xlim(left=start_tick + delta_tick, right=right_tick)
        st.pyplot(fig1)

        frcst = forecast.copy()

        forecast = forecast[['ds', 'yhat']].set_index('ds')
        forecast = forecast[930:]
        train = train[['ds', 'y']].set_index('ds')
        train.columns = ['y_train']
        test = test[['ds', 'y']].set_index('ds')
        test.columns = ['y_test']
        #df = pd.merge(forecast, train, left_index=True)
        #df = pd.concat([forecast, train, test])
        #df = df.fillna(0)
        df = train.join(forecast, how='outer').join(test, how='outer')
        st.line_chart(df[['yhat', 'y_train', 'y_test']])

    """## Trends, daily, weekly an yearly"""
    with st.expander("Show Trends:"):
        st.write(model.plot_components(frcst))

    """## Cross-Validation"""
    with st.expander("Show Metrics:"):
        df_cv_results = load_cv_results(CV_PATH, F_STREAM_DICT[feature_total])
        metric = st.radio("", ('mse', 'rmse', 'mae', 'mape', 'mdape', 'smape'),
                          horizontal=True, index=3)
        st.write(plot_cross_validation_metric(df_cv_results, metric=metric))

### Forecast ###
elif selected_page == "Forecast":
    """# Forecast"""

    proph_dict = load_model(model_name, path=MOODELS_PATH)
    ids = proph_dict.keys()
    """## Prophet Model"""
    slect_id = st.selectbox(f"Select a {PROPH[df_id_by]} id:", ids)
    with st.expander("Show Model:"):
        st.write(proph_dict[slect_id]['model'].plot(proph_dict[slect_id]['forecast']))

    """## Test, Train and Forecast Data"""
    #st.line_chart(df[['yhat', 'y_train', 'y_test']])
    fig2, ax2 = plt.subplots(figsize=(12, 6))

    st.write()

    plt.plot(proph_dict[slect_id]['train']['ds'], proph_dict[slect_id]['train']['y'], label="Train")
    plt.plot(proph_dict[slect_id]['test']['ds'], proph_dict[slect_id]['test']['y'], label="Train")
    plt.plot(proph_dict[slect_id]['forecast']['ds'][930:], proph_dict[slect_id]['forecast']['yhat'][930:], label="Train")
    plt.tick_params(axis='x', labelsize=12, rotation=45)
    plt.tick_params(axis='y', labelsize=12)

    # SLIDER to chage the plot
    start = st.slider("Selcet Range:", 0, 36, 0)
    start_tick = dt.datetime.strptime('2013-01', '%Y-%m').date()
    delta_tick = start*timedelta(days=28)
    right_tick = dt.datetime.strptime('2016-01', '%Y-%m').date()

    plt.xlim(left=start_tick + delta_tick, right=right_tick)
    st.pyplot(fig2)

### Predict ###
elif selected_page == "Predict":
    """# Results"""
    results = load_final_csv()
    """## Number of Sales by Shops, Categories, Items and Categories per Shop"""
    results['agg'].set_index('Unnamed: 0', inplace=True)
    results['agg'].astype('int')
    results['agg']

    """## Plot Distribution Chart"""
    with st.expander("Show Distribution by Shop:"):
        df_shop = results['shop'].drop(['Unnamed: 0'], axis=1)
        df_shop.set_index('shop_id', inplace=True)
        df_shop = df_shop.sort_values(by = "shops_n_sales", ascending=False).iloc[:60]
        df_shop = df_shop.T
        fig_shop = plt.figure(figsize=(12, 5))
        sns.barplot(df_shop)
        plt.tick_params(axis='x', labelsize=10, rotation=90)
        plt.tick_params(axis='y', labelsize=10)
        st.pyplot(fig_shop)

    with st.expander("Show Distribution by Categorie:"):
        df_cat = results['cat'].drop(['Unnamed: 0'], axis=1)
        df_cat.set_index('cat_id', inplace=True)
        df_cat = df_cat.sort_values(by = "cats_n_sales", ascending=False).iloc[:60]
        df_cat = df_cat.T
        fig_cat = plt.figure(figsize=(12, 5))
        sns.barplot(df_cat)
        plt.tick_params(axis='x', labelsize=10, rotation=90)
        plt.tick_params(axis='y', labelsize=10)
        st.pyplot(fig_cat)

    with st.expander("Show Distribution by Item:"):
        df_item = results['item'].drop(['Unnamed: 0'], axis=1)
        df_item.set_index('item_id', inplace=True)
        df_item = df_item.sort_values(by = "items_n_sales", ascending=False).iloc[:60]
        df_item = df_item.T
        fig_item = plt.figure(figsize=(12, 5))
        sns.barplot(df_item)
        plt.tick_params(axis='x', labelsize=10, rotation=90)
        plt.tick_params(axis='y', labelsize=10)
        st.pyplot(fig_item)

    with st.expander("Show Distribution by Categorie per Shop:"):
        df_catshop = results['cat_shop'].drop(['Unnamed: 0', 'Unnamed: 1'], axis=1)
        df_catshop[['shop_id', 'cat_id']] = df_catshop[['shop_id', 'cat_id']].astype('str')
        df_catshop['cat_shop'] = df_catshop.shop_id+"_"+df_catshop.cat_id
        df_catshop.set_index('cat_shop', inplace=True)
        df_catshop = df_catshop.drop(['shop_id', 'cat_id'], axis=1)
        df_catshop = df_catshop.sort_values(by = "cat_shops_n_sales", ascending=False).iloc[:60]
        df_catshop = df_catshop.T
        fig_catshop = plt.figure(figsize=(12, 5))
        sns.barplot(df_catshop)
        plt.tick_params(axis='x', labelsize=10, rotation=90)
        plt.tick_params(axis='y', labelsize=10)
        st.pyplot(fig_catshop)
