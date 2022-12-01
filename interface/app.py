
import streamlit as st
import os
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
sns.set()

import requests
import datetime as dt

from load_func import load_sales_df

from models.params import VERSION, STREAMLIT_PATH
from models.dict_vars import FEATURE_DICT, F_STREAM_DICT, DF_DICT, PERIOD_DICT

#st.set_page_config(layout='wide')
st.set_page_config(
    page_title="Le Wagon Project",
    page_icon="🐍",
    layout="centered",
    initial_sidebar_state="auto"
    )

st.sidebar.title("Blast from the Forecast")
selectedpage = st.sidebar.selectbox("Select the page",["Overview", "Forecast"])

if selectedpage == "Overview":
    """# Preliminary view of the Data Set"""
    columns = st.columns(4)
    df_id = columns[0].selectbox(
        "Choose a Data Frame:", ["Shop", "Categorie", "Item", "Categorie per Shop"])
    feature = columns[1].selectbox(
        "Choose a feature:", ["Item Count", "Total Value"])
    period = columns[2].selectbox(
        "Choose a period:", ["Day", "Week", "Month"])
    version = columns[3].text_input(
        "Choese a version", VERSION)
    file_name = "_".join([
        DF_DICT[df_id], F_STREAM_DICT[feature], PERIOD_DICT[period], version, ".csv"])
    st.write("File Name:", file_name)

    df = load_sales_df(DF_DICT[df_id],
        F_STREAM_DICT[feature],
        PERIOD_DICT[period],
        version,
        path=STREAMLIT_PATH)

    """## Plot Time Series"""
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

    st.altair_chart(df_sum)
