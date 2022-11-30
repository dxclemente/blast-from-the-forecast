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
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
db = os.getenv('DB')

# Remote or Local path
REMOTE = os.environ.get("REMOTE")

# Local CSV files names
CAT = os.environ.get("CAT")
ITEMS = os.environ.get("ITEMS")
SALES = os.environ.get("SALES")
SHOPS = os.environ.get("SHOPS")
TEST = os.environ.get("TEST")
SAMPLE = os.environ.get("SAMPLE")
# Local data path
DATA_PATH = os.environ.get("DATA_PATH")

# Prophet DFs file names by frequency
DF_DAY = os.environ.get("DF_DAY")
DF_WEEK = os.environ.get("DF_WEEK")
DF_MONTH = os.environ.get("DF_MONTH")
# Path to Save DFs
PATH_DF = os.environ.get("PATH_DF")

# Prophet Models params
LOADED = os.environ.get("LOADED")
SAVED = os.environ.get("SAVED")
# Path to save Models
PATH_MODELS = os.environ.get("PATH_MODELS")
