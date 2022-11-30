
import numpy as np
import pandas as pd

from models.prophet_model.preprocessor import (
    prep_sales_df, prep_categories_df, prep_items_df, prep_test_df
)

# from models.params import freq_analysis

# sort the Data Frame by shop/categore/item to be used in the analysis
def sort_sales(df_id: str, feature: str, period: str) -> pd.DataFrame:
    """
    Sort the Data Frame by shop/categore/item to be used in the analysis.
    df: Data Frame.
    name: shop_id, cat_id, item_id.
    feature: item_cnt_day, final_price.
    Period: {day: d, week: w, month: m}.
    """
    df = pd.pivot_table(
        prep_sales_df(), values=feature,
        index=[df_id], columns=['date'],
        aggfunc=np.sum
    )
    df = df.fillna(0).T
    df.columns = map(lambda i: df_id+"_"+str(i), df.columns)
    return df.resample(period).sum()

print(sort_sales('item_id', 'item_cnt_day', 'm'))
