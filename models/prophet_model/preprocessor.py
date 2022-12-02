
import pandas as pd

from models.data_sources.get_data import load_df

from models.params import CAT, ITEMS, SALES, TEST

# Preprocess sales_train
def prep_sales_df():
    sales_df = load_df(SALES)
    items_df = load_df(ITEMS)

    # column type to datetime
    sales_df["date"] = pd.to_datetime(sales_df.date, dayfirst=True)

    # merge sales_df with items_df on item_id
    sales_df = sales_df.merge(items_df[['item_id', 'item_category_id']], how='left', on='item_id')

    # rename item_category_id to cat_id
    sales_df.rename(columns={'item_category_id': 'cat_id'}, inplace=True)

    # create final price column and remove negative values
    sales_df['final_price'] = sales_df.item_cnt_day * sales_df.item_price
    sales_df.loc[sales_df['final_price'] < 0, ['final_price']] = 0

    # chage types
    sales_df = sales_df.astype({'item_cnt_day':'int32',
                                'date_block_num':'int32',
                                'shop_id':'int32',
                                'cat_id':'int32',
                                'item_id':'int32',
                                'item_price':'float32',
                                'final_price':'float32'})

    # sort by date
    sales_df.sort_values("date", inplace=True)
    return sales_df

# Preprocess item_categories_en
def prep_categories_df():
    # rename item_category_id to cat_id
    categories_df = load_df(CAT)
    categories_df.rename(columns={'item_category_id': 'cat_id'}, inplace=True)
    return categories_df

# Preprocess items_en
def prep_items_df():
    # rename item_category_id to cat_id
    items_df = load_df(ITEMS)
    items_df.rename(columns={'item_category_id': 'cat_id'}, inplace=True)
    return items_df

# Preprocess test
def prep_test_df():
    # merge test_df with item_df on item_id
    test_df = load_df(TEST)
    items_df = load_df(ITEMS)
    test_df = test_df.merge(items_df[['item_id', 'item_category_id']], how='left', on='item_id')
    test_df.rename(columns={'item_category_id': 'cat_id'}, inplace=True)
    return test_df

#check unique values from test_df and remove from sales_df
def prep_clean_sales_df():
    test_df = prep_test_df()
    unique_shops = test_df['shop_id'].unique()
    unique_cats = test_df['cat_id'].unique()
    unique_item = test_df['item_id'].unique()
    sales_df = prep_sales_df()
    sales_df = sales_df[
        sales_df['shop_id'].isin(unique_shops) &
        sales_df['cat_id'].isin(unique_cats) &
        sales_df['item_id'].isin(unique_item)
        ]
    return sales_df
