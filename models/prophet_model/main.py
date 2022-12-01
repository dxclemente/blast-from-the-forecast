
from itertools import product

from models.load_save.data_frame import load_sales_df, save_sales_df
from models.prophet_model.sort import sort_sales

from models.params import LOAD_DF, SAVE_DF, VERSION

# Data Frames Names:

def make_sale_df(df_id: str, feature: str, period: str):
    """"
    Load data, preprocess and sort number of sales or values of sales,
    for chosen combinations and period of time.
    df_id: shop_id, cat_id, item_id and cat_shop_id.
    feature:
        * number of sales: item_cnt_day
        * final price: final_price
    period: {day: d, week: w, month: m}.
    """
    # Load preprocessed Data Frame from local path
    if LOAD_DF == "load":
        load_sales_df(df_id, feature, period, VERSION)

    # get the data and run preprocess
    df = sort_sales(df_id, feature, period)

    if SAVE_DF == "save":
        save_sales_df(df, df_id, feature, period)

    return df

#print(make_sale_df(['shop_id', 'cat_id'], 'item_cnt_day', 'd'))

def make_all_save():
    df_id = ['shop_id', 'cat_id', 'item_id', ['cat_id', 'shop_id']]
    features = ['item_cnt_day', 'final_price']
    period = ['d', 'w', 'm']
    combinations = product(df_id, features, period)
    for comb in combinations:
        make_sale_df(*comb)
    return None

make_all_save()
