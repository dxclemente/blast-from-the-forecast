
import os

import pandas as pd

from models.params import VERSION, PATH_DF, STREAMLIT_PATH
from models.dict_vars import FEATURE_DICT, F_STREAM_DICT, DF_DICT, PERIOD_DICT

def load_sales_df(df_id, feature, period, version, path=PATH_DF):
    file_name = "_".join([df_id, feature, period, f"{version}.csv"])
    print(file_name)
    file_path = os.path.join(path, file_name)
    print(file_path)
    df = pd.read_csv(file_path)
    return df

def save_sales_df(df, df_id, feature, period):
    df_id = "".join(df_id).replace('id', "")[:-1]
    feature = FEATURE_DICT[feature]
    period = PERIOD_DICT[period]
    file_name = "_".join([df_id, feature, period, f"{VERSION}.csv"])
    file_path = os.path.join(PATH_DF, file_name)
    df.to_csv(file_path)
