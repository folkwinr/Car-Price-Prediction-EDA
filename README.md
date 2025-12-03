<div align="center">

# 🚗 AutoScout24 Car Listings  
### 🧹 From Raw Scraped JSON to Clean, Modeling-Ready Dataset

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776AB?logo=python&logoColor=white)]()
[![Pandas](https://img.shields.io/badge/pandas-Data%20Cleaning-150458?logo=pandas)]()
[![NumPy](https://img.shields.io/badge/numpy-Numerics-013243?logo=numpy)]()
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-F37626?logo=jupyter&logoColor=white)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)]()

**Goal:** Turn messy scraped car listings into a ✨ clean, well-structured dataset (`clean_scout2022.csv`)  
for price prediction, feature scoring, and exploratory analysis.

</div>

---

## 📌 TL;DR (Kısa Özet)

Bu proje, AutoScout24’ten scrape edilmiş ham JSON verisini:

- 🧹 temizliyor,
- 🧱 anlamlı kolonlara ayırıyor,
- 🧪 modellemeye uygun hale getiriyor,
- 📁 ve son olarak `clean_scout2022.csv` olarak dışa aktarıyor.

---

## 🗺️ Pipeline Overview

> The first part of the project focuses on building a **clean and modeling-ready** dataset from raw scraped car listings.

### 🧩 Step 1 – Setup & Data Import  
- Environment & library setup  
- Load `as24_cars.json` → `df0` → `df = df0.copy()`  
- First glance: `head`, `info`, `shape`, `columns`

### 🧩 Step 2 – Column Naming & Schema Cleanup  
- Fix messy group headers (`Comfort_Convenience`, `Extras`, `Safety_Security`, …)  
- Drop useless / empty header columns  
- Normalize all column names to `snake_case`

### 🧩 Step 3 – Missing Value Analysis & Column Pruning  
- Compute NaN ratios (`df_nans`)  
- Drop columns with extreme sparsity (> 80% NaN)  
- Remove fully empty rows  
- Detect suspicious `object` columns (`check_obj_columns`)

### 🧩 Step 4 – Column-wise Cleaning & Feature Engineering  
For each relevant column:  

> **Understand → Find problem → Clean → Engineer features → Final check**

Examples:
- `price` → numeric float  
- `first_registration` → `year` → `age = 2022 - year`  
- `power` → `power_kw` + `power_hp`  
- `fuel_consumption` → `cons_avg`, `cons_city`, `cons_country`  
- List columns (equipment) → `", "`-joined strings  
- Redundant ID / code columns → dropped

### 🧩 Step 5 – Final Validation & Export  
- Validate dtypes & feature set  
- Confirm ~58 → ~33 columns  
- Export: `clean_scout2022.csv`

---

## 📂 Project Structure

Önerilen klasör yapısı:

```text
.
├─ data/
│  ├─ raw/
│  │  └─ as24_cars.json         # raw scraped data (read-only)
│  ├─ interim/                  # optional intermediate CSVs
│  └─ processed/
│     └─ clean_scout2022.csv    # final cleaned dataset
├─ notebooks/
│  ├─ 01_setup_and_overview.ipynb
│  ├─ 02_schema_cleanup.ipynb
│  ├─ 03_missing_values.ipynb
│  └─ 04_column_cleaning_feature_eng.ipynb
├─ src/
│  └─ utils.py                  # df_nans, check_obj_columns, first_looking, ...
├─ reports/
│  └─ notes.md                  # data dictionary, decisions, TODOs
└─ README.md
