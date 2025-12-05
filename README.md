# ✨🚗 AutoScout24 Cars – Neon Data Cleaning & EDA Toolkit 🚀

> A visually guided, neon-styled project for **clean, readable, analysis-ready car data** using **Pandas**.

![Neon Data Vibes](https://media.giphy.com/media/l0IylOPCNkiqOgMyA/giphy.gif)

---

## 🌌 Project Overview

This project is a **mini data-cleaning toolkit** built around a real-world car listings dataset  
(e.g. from **AutoScout24** or similar sources).

The main goals are:

- 🧼 **Clean messy columns** (spaces, weird symbols, inconsistent names)
- 🧮 **Analyze missing values** at **DataFrame** and **column** level
- 🧱 Prepare the data for:
  - Exploratory Data Analysis (EDA)
  - Machine Learning models
  - Dashboards / reports

---

## 🧱 Key Components

### 1️⃣ `missing_values_tools.py`

Small helper module with functions to **inspect missing values**:

- `df_nans(df, limit)`  
  → Shows columns whose **missing percentage ≥ limit** (%).

- `show_missing_values(limit)`  
  → Wrapper around `df_nans(df, limit)` that uses a global `df`.

- `column_nans(serial)`  
  → Returns the **missing percentage** for a single column (`Series`).

> 💡 These tools make it easy to decide **which columns to drop, impute, or keep**.

---

## 🗂 Example Project Structure

    your-project/
    ├─ data/
    │  └─ as24_cars.json            # Raw car listings data
    ├─ notebooks/
    │  └─ 01_data_cleaning.ipynb
    ├─ src/
    │  ├─ missing_values_tools.py
    │  └─ column_cleaning_utils.py  # (optional; e.g. your own clean_columns_simple)
    └─ README.md

---

## ⚙️ Installation & Setup

Make sure you have **Python 3.9+** and **pip** installed.

Create and activate a virtual environment (optional but recommended):

    python -m venv .venv

On **Windows**:

    .venv\Scripts\activate

On **macOS / Linux**:

    source .venv/bin/activate

Install core dependency:

    pip install pandas

> 🧩 If you use extra tools (e.g. `skimpy`, `pyjanitor`, etc.), add them to `requirements.txt`.

---

## 🚦 Quick Start

### 🔹 1. Import the tools

In your notebook or script:

    import pandas as pd
    from src.missing_values_tools import df_nans, show_missing_values, column_nans

    # Example: load your dataset
    df = pd.read_json("data/as24_cars.json")

---

### 🔹 2. Check missing values for all columns

    # Show columns where missing % is >= 20
    high_missing = df_nans(df, limit=20)
    print(high_missing)

---

### 🔹 3. Quick helper using the global `df`

If you like using a global `df`:

    result = show_missing_values(limit=10)
    print(result)

---

### 🔹 4. Check missing values for a single column

    # Example: check missing % in the 'price' column
    missing_price = column_nans(df["price"])
    print(f"Missing values in 'price': {missing_price:.2f}%")

---

## 🧼 Typical Data-Cleaning Workflow

> A suggested neon-smooth pipeline for this project ⚡

1. **Load the raw data**

       df = pd.read_json("data/as24_cars.json")
       # If file is NDJSON style, use:
       # df = pd.read_json("data/as24_cars.json", lines=True)

2. **Normalize column names**

   Either with your own helper:

       from src.column_cleaning_utils import clean_columns_simple
       df = clean_columns_simple(df)

   Or with an external library like `skimpy` (if installed).

3. **Inspect missing values**

       df_nans(df, limit=10)
       column_nans(df["mileage_km"])

4. **Decide what to do**

   - Drop columns with too much missing data  
   - Impute or fill reasonable columns  
   - Keep important, clean features

5. **Save the cleaned dataset**

       df.to_csv("data/as24_cars_cleaned.csv", index=False)

---

## 🎨 Neon Visuals (Optional)

If you want to make your README even more cyber-vibe, you can add GIFs or images like:

    ![Neon dashboard](assets/neon-dashboard.gif)
    ![Glowing data grid](assets/neon-table.png)

> Place your files (e.g. `.gif`, `.png`) inside an `assets/` folder  
> and adjust the paths accordingly. GitHub will render them without any issues.

Example external GIF (already working):

![Neon Grid](https://media.giphy.com/media/26BRv0ThflsHCqDrG/giphy.gif)

---

## 🆚 Why Not Just Use `df.isnull()`?

You *can* manually do:

    null_percentages = df.isnull().sum() * 100 / df.shape[0]
    print(null_percentages)

But with this project’s helpers:

- `df_nans(df, limit=20)` → **directly focuses on problematic columns**  
- `column_nans(df["price"])` → **gives a clean % value for one feature**

This keeps your notebooks cleaner and your logic reusable.

---

## ✅ Goals of This Project

- 🔍 Make **data quality** issues visible (especially missing values)  
- 🧠 Encourage **clean code + small helper modules**  
- 🚀 Speed up **EDA and model preparation** for car listings data  
- 🎨 Keep it fun with **neon-style visuals & clean notebook layout**

---

## 🙌 Contributions

Feel free to:

- Add new helper functions (e.g. for outliers, type checking, etc.)  
- Improve documentation & examples  
- Share better visualizations / GIFs / dashboards  

> PRs, issues, and suggestions are always welcome 💜

---

## 💡 Inspiration

This project was built while exploring:

- Real-world JSON / NDJSON car listings  
- Practical Pandas data cleaning patterns  
- Reusable helper utilities for **missing values** and **column cleaning**

Happy cleaning & glowing! ✨

