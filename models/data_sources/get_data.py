
import os
from sqlalchemy import create_engine

import pandas as pd

from models.params import user, password, host, port, db
from models.params import SOURCE, DATA_PATH

# A long string that contains the necessary Postgres login information
def postgres_login():
    postgres_str = (
        'postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'
        .format(username=user,
                password=password,
                ipaddress=host,
                port=port,
                dbname=db)
        )
    cnx = create_engine(postgres_str)
    return cnx

# Read remote SQL tables names
def read_sql(file):
    cnx = postgres_login()
    query = f'SELECT * FROM {file};'
    df = pd.read_sql_query(query, cnx)
    return df

# Read Local CSV files names, in path
def read_path(file):
    file_name = os.path.join(DATA_PATH, file + '.csv')
    df = pd.read_csv(file_name)
    return df

# load remote or local file
def load_df(file):
    if SOURCE == 'remote':
        return read_sql(file)

    else:
        return read_path(file)
