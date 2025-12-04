"""
show_distribution.py

This file contains a helper function for Exploratory Data Analysis (EDA).
It prints basic statistics of a numeric column and shows two plots:
a histogram and a boxplot.

The goal is to help you understand:
- the shape of the data
- the central values (mean, median, mode)
- the minimum and maximum
- possible outliers

This file is ready to be imported in any notebook or script.
"""

import pandas as pd
import matplotlib.pyplot as plt
from termcolor import colored


def show_distribution(col):
    """
    Display the statistical summary, histogram, and boxplot for a numeric Pandas Series.

    Parameters
    ----------
    col : pandas.Series
        A numeric column from a DataFrame.

    Outputs
    -------
    Prints statistical values:
        - Minimum
        - Mean
        - Median
        - Mode
        - Maximum

    Plots:
        - Histogram with reference lines
        - Boxplot with mean, median, and outliers
    """

    # ------------------------------------------------
    # Calculate basic statistics
    # ------------------------------------------------
    min_val = col.min()
    max_val = col.max()
    mean_val = col.mean()
    med_val = col.median()
    mod_val = col.mode()[0]

    # ------------------------------------------------
    # Print statistics
    # ------------------------------------------------
    print(colored("Statistical Calculations :", "red", attrs=["bold"]))
    print(colored("-" * 26, "red", attrs=["bold"]))

    print(colored(
        f"Minimum: {min_val:>10.2f}\n"
        f"Mean:    {mean_val:>10.2f}\n"
        f"Median:  {med_val:>10.2f}\n"
        f"Mode:    {mod_val:>10.2f}\n"
        f"Maximum: {max_val:>10.2f}\n",
        "blue",
        attrs=["bold"]
    ))

    # ------------------------------------------------
    # Create the figure with two subplots
    # ------------------------------------------------
    fig, ax = plt.subplots(2, 1, figsize=(15, 15))

    # ------------------------------------------------
    # Histogram
    # ------------------------------------------------
    ax[0].hist(col, bins=30, edgecolor="black")
    ax[0].set_ylabel("Frequency", fontsize=10)

    # Add reference lines
    ax[0].axvline(min_val,  color="orange",     linestyle="--", linewidth=2, label="Minimum")
    ax[0].axvline(mean_val, color="lightgreen", linestyle="--", linewidth=2, label="Mean")
    ax[0].axvline(med_val,  color="cyan",       linestyle="--", linewidth=2, label="Median")
    ax[0].axvline(mod_val,  color="purple",     linestyle="--", linewidth=2, label="Mode")
    ax[0].axvline(max_val,  color="red",        linestyle="--", linewidth=2, label="Maximum")

    ax[0].legend(loc="upper right")

    # ------------------------------------------------
    # Boxplot
    # ------------------------------------------------
    medianprops = {"linestyle": "-", "linewidth": 3, "color": "m"}
    meanprops   = {"marker": "d", "markerfacecolor": "blue", "markeredgecolor": "black", "markersize": 10}
    flierprops  = {"marker": "o", "markersize": 8, "markerfacecolor": "fuchsia"}

    ax[1].boxplot(
        col,
        vert=False,
        notch=True,
        patch_artist=False,
        medianprops=medianprops,
        flierprops=flierprops,
        showmeans=True,
        meanprops=meanprops,
    )

    ax[1].set_xlabel("Value", fontsize=10)

    # ------------------------------------------------
    # Title
    # ------------------------------------------------
    fig.suptitle("Data Distribution", fontsize=20)
    plt.show()
