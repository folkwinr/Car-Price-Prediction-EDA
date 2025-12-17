"""
check_obj_columns.py

This file contains a helper function that checks all object-type columns
in a DataFrame and identifies if any of them contain mixed data types.
It prints:
- Column names with mixed types
- or "NO PROBLEM" if all object columns are consistent.
"""

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def check_obj_columns(df):
    '''
    Returns NO PROBLEM or column/s which has/have mixed object types.
    '''

    # Select only object columns and extract their types
    tdf = df.select_dtypes(include=['object']).applymap(type)

    mixed_columns = []  # store problematic columns

    # Check each object column
    for col in tdf:
        if len(set(tdf[col].values)) > 1:
            mixed_columns.append(col)

    # Print results
    if mixed_columns:
        for col in mixed_columns:
            print("Column " + color.BOLD + color.RED + col + color.END + " has mixed object types.")
    else:
        print(color.BOLD + color.GREEN + "NO PROBLEM" + color.END + " with the data types of Columns in the DataFrame.")
