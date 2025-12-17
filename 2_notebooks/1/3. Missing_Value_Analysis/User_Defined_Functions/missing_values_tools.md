# 📊 Missing Values Tools  
Simple helper functions for analyzing missing data in a Pandas DataFrame (B1–B1+ English)

---

## 📘 Overview  
This module contains three small functions that help you understand missing values in your dataset.  
They are useful during EDA (Exploratory Data Analysis), data cleaning, and preprocessing.

The functions do **not** change your data.  
They only calculate and display missing-value percentages.

---

## 1️⃣ `df_nans(df, limit)`  
**Purpose:**  
Returns the columns where the percentage of missing values is **greater than or equal** to the given limit.

### ✔ How it works:
1. `df.isnull()` → checks which cells are missing  
2. `.sum()` → counts missing values for each column  
3. `* 100 / df.shape[0]` → converts the count into a percentage  
4. `.loc[...]` → selects only the columns above the limit  

If no column exceeds the limit, the function returns:

> "No columns have missing values that exceed the given limit."

### ✔ Example:

    df_nans(df, 80)

---

## 2️⃣ `show_missing_values(limit)`  
A simple wrapper function around `df_nans()`.  
It uses the global DataFrame `df`.

So:

    show_missing_values(60)

is the same as:

    df_nans(df, 60)

This is useful when you want to check missing values quickly with one argument.

---

## 3️⃣ `column_nans(serial)`  
**Purpose:**  
Returns the missing-value percentage for **one single column**.

### ✔ Example:

    column_nans(df["power_hp"])

Example output:

    12.45

This means:  
12.45% of the values in the `power_hp` column are missing.

---

## ⭐ Why these tools are helpful?
- Quickly find columns with high missing values  
- Help you decide which columns to drop, clean, or impute  
- Good first step in EDA  
- Beginner-friendly and easy to use  

---

## 📁 Files Included

    missing_values_tools.py
    missing_values_tools.md

---

Happy Analyzing! 🚀
