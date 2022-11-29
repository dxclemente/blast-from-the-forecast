import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# bar plot function
def bar_plot_func(df: pd.core.frame.DataFrame, xlabel="", ylabel="", start=0) -> None:
    """
    Bar plot the data.
    data: dictionary with the values.
    """
    df = df.sum().sort_values(ascending=False)
    df = df.iloc[start:80+start]
    plt.figure(figsize=(12, 5))
    sns.barplot(x=df.index, y=df.values, order=df.index)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tick_params(axis='x', labelsize=6, rotation=90)
    plt.tick_params(axis='y', labelsize=10)
    plt.show()

# line plot function
def line_plot_func(df: pd.core.frame.DataFrame, number=2, sample: list=[], ylabel="") -> None:
    """
    Line plot the data.
    df: data frame to be ploted.
    number: number of randon samples.
    sample: a list with itens to be ploted, override number.
    """
    plt.figure(figsize=(12, 7))
    if sample:
        sns.lineplot(df.loc[:,sample])
    else:
        sns.lineplot(data=df.sample(number, axis=1))
    plt.xlabel("Date")
    plt.ylabel(ylabel)
    plt.tick_params(axis='x', labelsize=10, rotation=45)
    plt.tick_params(axis='y', labelsize=10)
    plt.legend(fontsize=10)
    plt.show()
