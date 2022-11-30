
# Merge with categories to get the Ids
sales_train_df = pd.merge(sales_train_df, items_df, left_on='item_id', right_on='item_id', how='left')

# Merge with cleaning_item_category_df to get the status of active and non active categories
sales_train_df = pd.merge(sales_train_df, cleaning_item_category_df, left_on='item_category_id', right_on='item_category_id', how='left')

# Merge with cleaning_store_df to get the status of active and non active shops
sales_train_df = pd.merge(sales_train_df, cleaning_store_df, left_on='shop_id', right_on='shop_id', how='left')

# Drop column that contais the items name, category status name, and shop status name
sales_train_df.drop(labels=['item_name', 'category_status','shop_status'], axis=1, inplace=True)

# Set date to YYYY/mm/dd
sales_train_df['date'] = pd.to_datetime(sales_train_df['date'], format='%d.%m.%Y')

# Set property dtypes for all other columns
sales_train_df = sales_train_df.astype({'date_block_num':'Int32',
                                        'shop_id':'Int32',
                                        'item_id':'Int32',
                                        'item_price':'float32',
                                        'item_cnt_day':'Int32',
                                        'item_category_id':'Int32',
                                        'category_status_code':'Int32',
                                        'shop_status_code':'Int32'})

# Set a new DataFrame to work with models
sales_train_clean_df = sales_train_df.copy()

# Filter only active categories and stores
sales_train_clean_df = sales_train_clean_df.query('category_status_code == 1').query('shop_status_code == 1')

# Drop category_status_code and shop_status_code to lightweight the dataframe
sales_train_clean_df.drop(labels=['category_status_code', 'shop_status_code'], axis=1, inplace=True)

# Drop duplicates, just in case
sales_train_clean_df.drop_duplicates(inplace=True)
