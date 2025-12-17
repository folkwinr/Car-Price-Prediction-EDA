# ============================================================
# 📊 MISSING VALUES HELPER TOOLS
# ============================================================
# This file contains three small helper functions to inspect
# missing values (NaN) in a Pandas DataFrame or Series.
#
# 🔧 Functions:
# 1) df_nans(df, limit)
#    → Shows columns whose missing-value percentage is >= limit.
#
# 2) show_missing_values(limit)
#    → Shortcut wrapper that calls df_nans(df, limit)
#      using the global DataFrame `df`.
#
# 3) column_nans(serial)
#    → Shows missing-value percentage for a single column.
# ============================================================

import pandas as pd


def df_nans(df, limit):
    """
    Return columns whose missing-value % is >= limit.
    """

    # --------------------------------------------------------
    # 🧮 STEPS (column-wise missing percentages)
    # 1. df.isnull()      → True/False for each cell (is NaN?)
    # 2. .sum()           → counts how many True (NaN) in each column
    # 3. * 100 / n_rows   → converts count into percentage
    # 4. .loc[lambda...]  → keeps only columns >= given limit
    # --------------------------------------------------------

    # missing % for each column
    missing = df.isnull().sum() * 100 / df.shape[0]

    # keep only columns above the limit
    missing = missing.loc[lambda x: x >= limit]

    # if nothing matches, return a short message
    if missing.empty:
        return "No columns have missing values that exceed the given limit."

    return missing


def show_missing_values(limit):
    """
    Shortcut: use global df with df_nans().
    """

    # Calls df_nans() using a preset/global DataFrame named `df`
    return df_nans(df, limit)


def column_nans(serial):
    """
    Return missing-value % for a single Series.
    """

    # Same logic as df_nans but for ONE column:
    # isnull() → sum() → *100 / number of rows
    return serial.isnull().sum() * 100 / serial.shape[0]
