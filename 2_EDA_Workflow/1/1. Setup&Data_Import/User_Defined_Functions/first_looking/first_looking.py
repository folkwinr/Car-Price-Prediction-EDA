"""
first_looking.py

A helper function for quick inspection of a DataFrame column.
It prints basic information such as:
- null percentage
- number of nulls
- number of unique values
- DataFrame shape
- value counts for the selected column

Useful for initial EDA (Exploratory Data Analysis).
"""

import pandas as pd


def first_looking(df, col):
    """
    Print basic information about a column in a Pandas DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to analyze.
    col : str
        The name of the column to inspect.

    Prints
    ------
    - Column name
    - Percentage of null values
    - Number of null values
    - Number of unique values
    - Shape of the DataFrame
    - Value counts (including NaN)
    """

    print("Column Name     :", col)
    print("--------------------------------")
    print("Percent Nulls   :", "%", round(df[col].isnull().sum() * 100 / df.shape[0], 2))
    print("Number Nulls    :", df[col].isnull().sum())
    print("Unique Values   :", df[col].astype(str).nunique())
    print("DataFrame Shape :", df.shape)
    print("--------------------------------")
    print(df[col].value_counts(dropna=False))
