"""
Postgres
Model
Prophet Model package params
load and validate the environment variables in the `.env`
"""

import os
from dotenv import load_dotenv

# Set postgres credentials
load_dotenv()
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db = os.getenv("DB")

# Local CSV files and remote SQL tabled names
SHOPS = "shops_en"
CAT = "item_categories_en"
ITEMS = "items_en"
SALES = "sales_train"
TEST = "test"
SAMPLE = "sample_submission"
CLR_STORE = "cleaning_store_id"
CLR_ITEM_CAT = "cleaning_item_category_id"
# Local raw data path
DATA_PATH = "raw_data"

## Prophet model parans:
# Load preprocessed Data Frame from local path
LOAD_DF = "no" # or "load" the the data from path
PATH_DF = "raw_data/prophet_df"
STREAMLIT_PATH = "../raw_data/prophet_df"

CV_PATH = "../raw_data/cross_val"
MOODELS_PATH = "../raw_data/prophet"

# If there is no local sales_df data,
# Load raw data from remote or local path to preprocess
SOURCE = "local" # or "remote"

# Save sales, values data frame
SAVE_DF = "save"
FEATURE_DICT = {"item_cnt_day": "n_sales", "final_price": "value"}
F_STREAM_DICT = {"Item_Cont": "n_sales", "Total_Value": "value"}
PERIOD_DICT = {"d": "day", "w": "week", "m": "month"}
VERSION = "v01"

# Prophet DFs file names by frequency
DAY = "day"
WEEK = "week"
MONTH = "month"

# Sales Data Frame Files Names
# Prophet Models params
LOADED = "load"
SAVED = "save"
# Path to save Models
PATH_MODELS = "/raw_data/prophet"
