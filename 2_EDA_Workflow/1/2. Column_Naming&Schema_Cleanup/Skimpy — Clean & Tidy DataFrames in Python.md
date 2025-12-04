# 📘 Skimpy — Clean & Tidy DataFrames in Python  
*A small but powerful toolkit for automated DataFrame cleaning*

---

## 🌟 What Is Skimpy?

**Skimpy** is a lightweight Python library that helps you quickly **clean**, **standardize**, and **summarize** Pandas DataFrames.

Use Skimpy when you have:

- 🌀 Messy or inconsistent **column names**
- 🧹 String values that need **cleaning / normalization**
- 🔣 Columns containing **special characters, spaces, or weird formatting**
- ⚙️ Large datasets that require **fast automatic preprocessing**

> ✅ Goal: Turn a messy DataFrame into an **analysis-ready DataFrame** with just a few commands.

---

## 🛠️ Installation

~~~bash
pip install skimpy
~~~

Import the main tools:

~~~python
from skimpy import clean_columns, clean_strings, clean_df, skim
~~~

---

## 🔧 Core Functions in Skimpy

---

### 1️⃣ `clean_columns(df)`

Cleans and standardizes **column names**.

#### 🔍 What it does

- Converts names to **lowercase**
- Replaces spaces and punctuation with **snake_case**  

  - `"Body type"` → `body_type`  
  - `"Country Version "` → `country_version`  
  - `"Mileage(km)"` → `mileage_km`  
  - `" Offer number?? "` → `offer_number`  
  - `"Power [KW]"` → `power_kw`

- Removes unwanted characters: `()`, `[]`, `?`, `.`, `-`, etc.
- Strips leading/trailing whitespace
- Normalizes unicode characters

#### 💻 Example

~~~python
from skimpy import clean_columns

df = clean_columns(df)
~~~

After this, all column names are:

- consistent  
- easy to type  
- ready for further processing  

---

### 2️⃣ `clean_strings(df)`

Cleans **string values** inside the DataFrame (not just column names).

#### 🔍 What it does

- Strips extra spaces (`"  text   "` → `"text"`)
- Normalizes unicode characters
- Fixes irregular spacing
- Makes string data more consistent for analysis

#### 💻 Example

~~~python
from skimpy import clean_strings

df = clean_strings(df)
~~~

This is useful when many columns contain messy text like:

- `"  Mercedes-Benz "`  
- `"BMW\n"`  
- `"  120 000  km  "`  

---

### 3️⃣ `clean_df(df)`

Runs a **full cleaning pipeline** on the DataFrame.

> 🧼 `clean_df` = `clean_columns` + `clean_strings` in one step.

#### 💻 Example

~~~python
from skimpy import clean_df

df = clean_df(df)
~~~

This will:

- clean all **column names**
- clean all **string values**
- give you a **tidier DataFrame** with one function call

Perfect as a **first step** after loading a raw dataset.

---

### 4️⃣ `skim(df)`

Provides a nice **summary** of your DataFrame (similar to R’s `skimr`).

#### 🔍 What it shows

- Number of rows / columns  
- Data types  
- Missing values  
- Basic distribution info for each column  

#### 💻 Example

~~~python
from skimpy import skim

skim(df)
~~~

This is helpful for a quick **EDA (Exploratory Data Analysis)** overview.

---

## 🆚 `rename()` vs Skimpy

Sometimes you might consider using `pandas.DataFrame.rename()` instead of Skimpy.

### 🔁 `rename()` (manual)

- You must **manually** specify each column name you want to change.
- Good for **a few columns**, but painful for 30–50+ columns.

~~~python
df = df.rename(columns={
    "Body type": "body_type",
    "Country version": "country_version",
})
~~~

### ⚡ Skimpy (automatic)

- Cleans **all** column names at once.
- No need to write every old and new name manually.
- Great for **large**, messy datasets.

---

### 📊 Comparison Table

| Feature / Task                              | `rename()` (Pandas) | Skimpy (`clean_columns`, `clean_df`) |
|--------------------------------------------|----------------------|--------------------------------------|
| Automatic cleanup of all column names      | ❌ No                | ✅ Yes                               |
| Convert to lowercase                       | ❌ Manual            | ✅ Automatic                         |
| Replace spaces with `snake_case`           | ❌ Manual            | ✅ Automatic                         |
| Remove special characters                  | ❌ Manual            | ✅ Automatic                         |
| Clean string values inside the DataFrame   | ❌ No                | ✅ Yes (`clean_strings`, `clean_df`) |
| Good for 50+ messy columns                 | 😭 Very tedious      | 😎 Very easy                         |

---

## 🧠 When Should You Use Skimpy?

Use Skimpy as an **early preprocessing step** when:

- You just loaded a JSON/CSV file and columns look ugly or inconsistent  
- You see names like `"  First registration (date)"`, `"Offer number??"`, `"Mileage (KM)"`  
- You want to avoid bugs caused by spaces or strange characters in column names  
- You will later build **ML models** or do **groupby / merge / joins**, and need clean labels

---

## 🏁 Summary

- **Skimpy** is a tiny but powerful library for **cleaning DataFrames**.  
- It focuses on:
  - 🧼 Cleaning column names  
  - 🧼 Cleaning string values  
  - 📊 Quickly summarizing data  

> ⚡ One or two commands can turn a raw, messy dataset into a clean, consistent, analysis-ready DataFrame.

Recommended typical usage:

~~~python
from skimpy import clean_df, skim

df = clean_df(df)  # full clean (columns + strings)
skim(df)           # quick overview of the cleaned data
~~~
