# 📊 show_distribution() Function  
*A simple and helpful tool for Exploratory Data Analysis (EDA)*

---

## 🔎 Overview  
The `show_distribution()` function helps you understand a numeric column in your dataset.  
It prints basic statistics and shows two visual plots:

- a **Histogram** → shows the shape of the data  
- a **Boxplot** → shows the spread of the data and possible outliers  

This tool is useful before applying deeper analysis or machine learning models.

---

## 📈 What the function does

### ✔ Prints basic statistics:
- Minimum  
- Mean  
- Median  
- Mode  
- Maximum  

These values help you understand the “central tendency” and the range of the column.

---

### ✔ Shows two plots:
#### 1) **Histogram**
This plot shows how often each value appears.  
It also draws vertical lines for:
- Min
- Mean
- Median
- Mode
- Max

#### 2) **Boxplot**
This plot shows:
- the median line  
- the mean marker  
- the distribution spread  
- the outliers  

---

## 🧪 Example Usage

```python
from show_distribution import show_distribution
import pandas as pd

sample = pd.Series([10, 20, 20, 25, 30, 40, 100])
show_distribution(sample)
