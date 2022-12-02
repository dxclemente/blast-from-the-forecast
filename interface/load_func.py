import os
import streamlit as st

import pandas as pd
import numpy as np

import pickle
import json
import gzip

from fixprophet.fixserialize import fix_model_from_json, fix_model_from_dict

from models.params import VERSION, PATH_DF, STREAMLIT_PATH
from models.dict_vars import FEATURE_DICT, F_STREAM_DICT, DF_DICT, PERIOD_DICT

@st.cache
def load_sales_df(df_id, feature, period, version, path):
    file_name = "_".join([df_id, feature, period, f"{version}.csv"])
    print(file_name)
    file_path = os.path.join(path, file_name)
    print(file_path)
    df = pd.read_csv(file_path, parse_dates=['date'])
    df = df.set_index('date')
    return df

@st.cache
def load_cross_val(path, feature, key, file_format):
    """"
    key = ['model', 'forecast', 'train', 'test', 'horizon']
    file_format = ['.gz', '.csv', '.pkl']
    """
    file_name = "_".join(["prophet_total", feature, key+file_format])
    file_name = os.path.join(path, file_name)

    if file_format == '.gz':
        with gzip.open(file_name, 'rt') as mdl:
            model = fix_model_from_json(json.load(mdl))
        return model
    elif file_format == '.csv':
        df = pd.read_csv(file_name)
        df['ds'] = pd.to_datetime(df.ds)
        return df
    elif file_format == '.pkl':
        with open((file_name), 'rb') as hrzn:
            horizon = pickle.load(hrzn)
        return horizon
    return None

@st.cache
def load_cv_results(path, feature):
    """
    feature: {"Item Count": "n_sales", "Total Value": "value"}
    """
    cv_name = "_".join(['cv', feature, 'results.csv'])
    full_path = os.path.join(path, cv_name)
    df = pd.read_csv(full_path)
    df['ds'] = pd.to_datetime(df.ds)
    df['cutoff'] = pd.to_datetime(df.cutoff)
    df.drop(['Unnamed: 0'], axis=1, inplace=True)
    return df

# Load models from file
def load_model(file_name: str, path) -> dict:
    path_model = os.path.join(path, file_name + "_model.gz")
    path_forecast = os.path.join(path, file_name + "_forecast.gz")
    path_train = os.path.join(path, file_name + "_train.gz")
    path_test = os.path.join(path, file_name + "_test.gz")
    path_horizon = os.path.join(path, file_name + "_horizon.pkl")

    with gzip.open(path_model, 'rt') as mdl:
        model = json.load(mdl)
    with gzip.open(path_forecast, 'rt') as frct:
        forecast = json.load(frct)
    with gzip.open(path_train, 'rt') as trn:
        train = json.load(trn)
    with gzip.open(path_test, 'rt') as tst:
        test = json.load(tst)
    with open(path_horizon, 'rb') as hrzn:
        horizon = pickle.load(hrzn)
    results = {}
    for id in model:
        prophet_dict = {}
        prophet_dict = {
            'model': fix_model_from_json(model[id]),
            'forecast': pd.read_json(forecast[id]),
            'train': pd.read_json(train[id]),
            'test': pd.read_json(test[id]),
            'horizon': int(horizon[int(id)])
        }
        prophet_dict['forecast']['ds'] = pd.to_datetime(prophet_dict['forecast'].ds, unit='ms')
        prophet_dict['train']['ds'] = pd.to_datetime(prophet_dict['train'].ds, unit='ms')
        prophet_dict['test']['ds'] = pd.to_datetime(prophet_dict['test'].ds, unit='ms')
        results[id] = prophet_dict

    return results

# Load finals csv
def load_final_csv():
    shops_pred = pd.read_csv("../raw_data/prophet/shops_pred.csv")
    cat_pred = pd.read_csv("../raw_data/prophet/cat_pred.csv")
    items_pred = pd.read_csv("../raw_data/prophet/items_pred.csv")
    cats_shops_pred = pd.read_csv("../raw_data/prophet/cats_shops_pred.csv")
    pred_agg_total = pd.read_csv("../raw_data/prophet/pred_agg_total.csv")

    results = {'agg': pred_agg_total, 'shop': shops_pred, 'cat': cat_pred,
               'item': items_pred, 'cat_shop': cats_shops_pred}

    return results
