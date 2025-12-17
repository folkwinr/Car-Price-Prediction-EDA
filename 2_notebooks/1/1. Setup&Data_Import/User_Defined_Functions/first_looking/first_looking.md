# 🔍 first_looking() Function  
*A simple helper for quick column inspection*

---

## 📘 Overview  
The `first_looking()` function gives a fast summary of any column in a Pandas DataFrame.  
It is useful in the early steps of **Exploratory Data Analysis (EDA)**.

You pass:
- a DataFrame (`df`)
- a column name (`col`)

The function prints basic but important information about that column.

---

## 📊 What the Function Prints

### ✔ Column Name  
Shows which column is being inspected.

### ✔ Percent of Null Values  
Tells you how much of the column is missing (0–100%).

### ✔ Number of Null Values  
Exact count of missing entries.

### ✔ Number of Unique Values  
How many different values appear in the column.

### ✔ DataFrame Shape  
Total rows and columns of the dataset.

### ✔ Value Counts  
How many times each value appears.  
`dropna=False` ensures NaN values are also shown.

---

## 🧪 Example Usage

```python
from first_looking import first_looking

first_looking(df, "fuel_type")


Column Name     : fuel_type
--------------------------------
Percent Nulls   : % 12.5
Number Nulls    : 210
Unique Values   : 6
DataFrame Shape : (15000, 25)
--------------------------------
diesel    7000
petrol    6000
NaN       210
hybrid    150
electric   80
LPG        60


