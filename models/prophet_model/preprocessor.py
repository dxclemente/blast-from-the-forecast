
import pandas as pd

# column type to datetime
sales_local_df["date"] = pd.to_datetime(sales_local_df.date, dayfirst=True)

# rename item_category_id to cat_id
categories_local_df.rename(columns={'item_category_id': 'cat_id'}, inplace=True)
items_local_df.rename(columns={'item_category_id': 'cat_id'}, inplace=True)
sales_local_df.rename(columns={'item_category_id': 'cat_id'}, inplace=True)

# merge test_local_df with item_df on item_id
test_local_df = test_local_df.merge(items_local_df[['item_id', 'cat_id']], how='left', on='item_id')

# merge items_local_df with sales_local_df on item_id
sales_local_df = sales_local_df.merge(items_local_df[['item_id', 'cat_id']], on='item_id')

# chage types
sales_local_df['item_cnt_day'] = sales_local_df['item_cnt_day'].astype('int32')
sales_local_df['date_block_num'] = sales_local_df['date_block_num'].astype('int32')
sales_local_df['shop_id'] = sales_local_df['shop_id'].astype('int32')
sales_local_df['item_id'] = sales_local_df['item_id'].astype('int32')
sales_local_df['cat_id'] = sales_local_df['cat_id'].astype('int32')
sales_local_df['item_price'] = sales_local_df['item_price'].astype('float32')

# create final price column and remove negative values
sales_local_df['final_price'] = sales_local_df.item_cnt_day * sales_local_df.item_price
sales_local_df['final_price'] = sales_local_df['final_price'].astype('float32')
sales_local_df.loc[sales_local_df['final_price'] < 0, ['final_price']] = 0

# sort by date
sales_local_df.sort_values("date", inplace=True)
