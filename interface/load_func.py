import os
import streamlit as st

import pandas as pd
import numpy as np

from models.params import VERSION, PATH_DF, STREAMLIT_PATH
from models.dict_vars import FEATURE_DICT, F_STREAM_DICT, DF_DICT, PERIOD_DICT

@st.cache
def load_sales_df(df_id, feature, period, version, path=PATH_DF):
    file_name = "_".join([df_id, feature, period, f"{version}.csv"])
    print(file_name)
    file_path = os.path.join(path, file_name)
    print(file_path)
    df = pd.read_csv(file_path, parse_dates=['date'])
    df = df.set_index('date')
    return df

#headers = ['col1', 'col2', 'col3', 'col4']
#dtypes = ['datetime', 'datetime', 'str', 'float']
#pd.read_csv(file, sep='\t', header=None, names=headers, dtype=dtypes)
#
#headers = ['col1', 'col2', 'col3', 'col4']
#dtypes = {'col1': 'str', 'col2': 'str', 'col3': 'str', 'col4': 'float'}
#parse_dates = ['col1', 'col2']
#pd.read_csv(file, sep='\t', header=None, names=headers, dtype=dtypes, parse_dates=parse_dates)
