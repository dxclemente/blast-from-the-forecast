import pandas as pd

from models.prophet_model.params import freq_analysis

# sort the Data Frame by "types" to be used in the analysis
def sort_sales(df: pd.core.frame.DataFrame, name: str, feature: str) -> pd.core.frame.DataFrame:
    """
    Sort the Data Frame by "type(name)" to be used in the analysis.
    df: Data Frame.
    name: shop, cat, item.
    feature: item_cnt_day, final_price.
    """

    df_feature = pd.DataFrame()

    for id in range(df.shape[0]):
        name_id = f'{name}_id_{id}'
        df = sales_local_df[sales_local_df[f'{name}_id'] == id]
        df = df.resample(freq_analysis, on='date').sum()[[feature]]
        df.rename(columns = {feature:name_id}, inplace=True)
        df_feature = pd.concat([df_feature, df], axis=1)

    return df_feature
