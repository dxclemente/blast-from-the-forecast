
import numpy as np
import pandas as pd

from models.prophet_model.preprocessor import (
    prep_clean_sales_df, prep_categories_df, prep_items_df, prep_test_df
)

# from models.params import freq_analysis

# sort the Data Frame by shop/categore/item to be used in the analysis
def sort_sales(df_id: str, feature: str, period: str) -> pd.DataFrame:
    """
    Sort number of sales or values of sales,
    for chosen combinations and period of time.
    df_id: shop_id, cat_id, item_id.
    feature:
        * number of sales: item_cnt_day
        * final price: final_price
    period: {day: d, week: w, month: m}.
    """
    sales_df = pd.pivot_table(
        prep_clean_sales_df(), values=feature,
        index=df_id, columns=['date'],
        aggfunc=np.sum
    )
    sales_df = sales_df.fillna(0).T
    df_id = "".join(df_id).replace('id', "")
    sales_df.columns = map(lambda i: df_id+"id_"+str(i), sales_df.columns)
    return sales_df.resample(period).sum()
