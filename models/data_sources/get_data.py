# Env
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import psycopg2

import pandas as pd

from models.prophet_model.params import REMOTE, PATH

# Set postgres credentials
load_dotenv()
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
db = os.getenv('DB')

# A long string that contains the necessary Postgres login information
postgres_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'
                .format(username=user,
                        password=password,
                        ipaddress=host,
                        port=port,
                        dbname=db))
cnx = create_engine(postgres_str)

# List DB tables
conn = psycopg2.connect(postgres_str)
cursor = conn.cursor()
cursor.execute("""SELECT relname FROM pg_class WHERE relkind='r'
                  AND relname !~ '^(pg_|sql_)';""") # "rel" is short for relation.

tables_list = [i[0] for i in cursor.fetchall()] # A list() of tables.
#tables_list #check available tables



# Load datasets
def load_data():
    if REMOTE:
        shops_df = pd.read_sql_query('''SELECT * FROM shops_en;''', cnx)
        item_categories_df = pd.read_sql_query('''SELECT * FROM item_categories_en;''', cnx)
        test_df = pd.read_sql_query('''SELECT * FROM test;''', cnx)
        sales_train_df = pd.read_sql_query('''SELECT * FROM sales_train;''', cnx)
        items_df = pd.read_sql_query('''SELECT * FROM items_en;''', cnx)
        cleaning_store_df = pd.read_sql_query('''SELECT * FROM cleaning_store_id;''', cnx)
        cleaning_item_category_df = pd.read_sql_query('''SELECT * FROM cleaning_item_category_id;''', cnx)

        # Prophet Model
        categories_ = item_categories_df.copy()
        items_ = items_df.copy()
        sales_ = sales_train_df.copy()
        shops_ = shops_df.copy()
        test_ = test_df.copy()
        sample_ = pd.DataFrame()

    else:
        categories_ = pd.read_csv(os.path.join(PATH, "item_categories.csv"))
        items_ = pd.read_csv(os.path.join(PATH, "items.csv"))
        sales_ = pd.read_csv(os.path.join(PATH, "sales_train.csv"))
        shops_ = pd.read_csv(os.path.join(PATH, "shops.csv"))
        test_ = pd.read_csv(os.path.join(PATH, "test.csv"))
        sample_ = pd.read_csv(os.path.join(PATH, "sample_submission.csv"))

    categories_local_df = categories_.copy()
    items_local_df = items_.copy()
    shops_local_df = shops_.copy()
    sales_local_df = sales_.copy()
    test_local_df = test_.copy()
    sample_local_df = sample_.copy()
