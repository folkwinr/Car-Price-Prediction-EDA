# 🚗 Car Price Prediction EDA (AutoScout24) — 3-Phase Data Preparation Pipeline

A complete, step-by-step data preparation project for car listings data, built as an EDA capstone.

✅ **Phase 1:** Data Cleaning  
✅ **Phase 2:** Handling Missing Values  
✅ **Phase 3:** Handling Outliers + Final Sanity Checks (**END OF PROJECT**)

> ⚠️ **Important Scope Note**  
> The project **ends after Phase 3 “Final Step”** (outlier handling + correlation check + duplicate removal).  
> We **do not include**: Business Questions, Inferential Statistics, or Dummy/Encoding steps.

---

## 📌 Table of Contents
- [🎯 Project Goal](#-project-goal)
- [🧾 Dataset](#-dataset)
- [🗂 Repository Structure](#-repository-structure)
- [🔄 Workflow Overview](#-workflow-overview)
  - [Phase 1 — 🧼 Data Cleaning](#phase-1--data-cleaning)
  - [Phase 2 — 🧩 Handling Missing Values](#phase-2--handling-missing-values)
  - [Phase 3 — 🚨 Handling Outliers + Final Step](#phase-3--handling-outliers--final-step)
- [📦 Outputs](#-outputs)
- [▶️ How to Run](#️-how-to-run)
- [🧠 Key Design Decisions](#-key-design-decisions)
- [⚠️ Limitations](#️-limitations)
- [🚀 Next Steps (Optional)](#-next-steps-optional)

---

## 🎯 Project Goal
Prepare messy, real-world car listing data for analysis and modeling by:
- cleaning formats and data types,
- handling missing values with smart, explainable rules,
- detecting and handling outliers using domain knowledge + robust statistics,
- removing duplicates and checking strong correlations in the final dataset.

---

## 🧾 Dataset
**Source format:** JSON (`as24_cars.json`)  
**Domain:** second-hand car listings (AutoScout24-style structure)

Typical feature groups:
- **Identity:** make/model/make_model  
- **Listing:** price, seller, location  
- **Technical:** engine_size, power_kW, gearbox, gears, drivetrain, empty_weight  
- **Usage:** mileage, age, previous_owner  
- **Eco:** fuel_type, co_emissions, cons_avg  
- **History/Other:** full_service_history, warranty, extras, upholstery, energy class

---

## 🗂 Repository Structure
Recommended structure (you can adjust names as you like):

```text
├─ notebooks/
│  ├─ EDA_scout_car_phase_1 (Data_Cleaning)_ONDIA.ipynb
│  ├─ EDA_scout_car_phase_2 (Handling_Missing_Values)_ONDIA.ipynb
│  └─ EDA_scout_car_phase_3 (Handling_Outliers)_ONDIA_V2.ipynb
│
├─ data/
│  └─ as24_cars.json
│
├─ outputs/
│  ├─ clean_scout2022.csv
│  └─ filled_scout2022.csv
│
└─ README.md
```

---

## 🔄 Workflow Overview

### Phase 1 — 🧼 Data Cleaning
**Notebook:** `EDA_scout_car_phase_1 (Data_Cleaning)_ONDIA.ipynb`  
**Input:** `as24_cars.json`  
**Output:** `clean_scout2022.csv`

What we did:
- 🔤 **Standardized column names** (snake_case) and checked mixed types.
- 🧹 **Cleaned key fields** (format fixes, consistent text formatting, safe conversions).
- 🔢 Converted numeric-like text into real numeric columns (price, mileage, engine_size, etc.).
- 🧠 Built early feature engineering where needed (example: split power and consumption fields).
- 🗑 Dropped columns that were:
  - extremely missing,
  - irrelevant for analysis,
  - ID/leakage-like (example: offer number),
  - free-text not used in this phase.
- ✅ Produced a clean baseline dataset ready for a strong missing-value strategy.

📦 **Export:** `clean_scout2022.csv`

---

### Phase 2 — 🧩 Handling Missing Values
**Notebook:** `EDA_scout_car_phase_2 (Handling_Missing_Values)_ONDIA.ipynb`  
**Input:** `clean_scout2022.csv`  
**Output:** `filled_scout2022.csv`

Main idea:
> Missing values are not filled randomly. We fill them using **car segment context**.

What we did (high-impact steps):
- 🧠 **Fixed group keys first** (because the whole filling logic depends on them):
  - repaired missing `model` using **regex extraction** from `short_description`,
  - rebuilt `make_model = make + model`,
  - standardized formatting (Title Case) for consistent grouping.
- 🧮 **Used different fill methods based on column type:**
  - **Mode** for categorical columns (doors, gearbox, fuel_type, drivetrain, seats, etc.),
  - **Median** for skewed numeric columns (co_emissions, cons_avg),
  - **Mean** for mileage inside strong segments (`make_model + age`),
  - **ffill/bfill** inside groups for propagation-like fields (previous_owner, upholstery).
- ⚡ **Applied Electric-car domain rules**
  - handled special behavior for `co_emissions` and `cons_avg` to avoid wrong values.
- 🧪 **Feature engineering during filling**
  - built package-level features from long equipment text:
    - `comfort_convenience_Package`
    - `entertainment_media_Package`
    - `safety_security_Package`
  - dropped raw long-text columns after creating better features (less noise).
- 🗑 Dropped redundant or low-value columns to keep the dataset focused:
  - redundant: `power_hp` (kept `power_kW`),
  - redundant: `cons_city`, `cons_country` (kept `cons_avg`),
  - low-value: `cylinders`,
  - helper columns used only for repair.

📦 **Export:** `filled_scout2022.csv`

---

### Phase 3 — 🚨 Handling Outliers + Final Step
**Notebook:** `EDA_scout_car_phase_3 (Handling_Outliers)_ONDIA_V2.ipynb`  
**Input:** `filled_scout2022.csv`  
**Output:** Final DataFrame after outliers + final checks (**END OF PROJECT**)

Core philosophy:
> Outliers are not all the same. Some are real, some are data errors, and some harm model quality.  
> We used a mix of **domain rules** and **robust statistics** to handle them.

#### 1) Outlier detection tools we used
- 🧠 **Domain rules** (impossible/unrealistic values)
- 📏 **Tukey’s Fence (IQR)** for heavy-tailed variables
- 🧮 **z-score style filtering** for extreme numeric cases

#### 2) Column-level outlier actions (what we did)
✅ **price**
- Removed clear anomaly cases by domain filters (specific `make_model` + extreme price levels).
- Applied **Tukey Fence** (IQR) and removed remaining extreme rows.

✅ **mileage**
- Dropped mileage values above **1,000,000** (domain-based).
- Applied **Tukey Fence** to remove extreme mileage rows.

✅ **engine_size**
- Marked known invalid values as **NaN** (very small or extremely large values).
- Filled missing using segment **mode** (`make_model + body_type`).
- Applied z-score filtering to remove remaining extreme rows.

✅ **gears**
- Set `gears == 0` or `gears > 8` to **NaN**, then filled with segment **mode**.
- Dropped `gears == 2` cases (treated as suspicious in this dataset).

✅ **empty_weight**
- Set `empty_weight > 4000` to **NaN**.
- Replaced known invalid values (example: 75, 525) with **NaN**.
- Filled missing using segment **mode**.

✅ **co_emissions**
- Marked specific extreme emissions values as **NaN** (example: 940, 910, 420, 414).
- Filled via segment **median**.
- Used `log1p` inspection to review distribution behavior.
- Applied z-score filtering for the most extreme rows.

✅ **cons_avg**
- Set values `>= 20` to **NaN** (domain-based).
- Filled via segment **median**.
- Applied z-score filtering for extreme rows.

✅ **previous_owner**
- Dropped rows where `previous_owner >= 10` (treated as extreme/unreliable).

✅ **age**
- Dropped rows where `age > 20` or `age < 0`.

🗑 Dropped columns during Phase 3:
- `doors`
- `seats`

#### 3) Final Step (end of project)
After outlier handling:
- 🔥 Checked correlation structure to understand strong relationships.
- 🧾 Checked duplicates and removed them:
  - `df.drop_duplicates(inplace=True)`

✅ This is the final point of the project pipeline.

> 💾 Optional: if you want to save the final dataset, add this line at the end of Phase 3:
```python
df.to_csv("scout_outliers_handled_final.csv", index=False)
```

---

## 📦 Outputs
- ✅ `clean_scout2022.csv` → output of Phase 1  
- ✅ `filled_scout2022.csv` → output of Phase 2  
- ✅ Final DataFrame after Phase 3 → outliers handled + duplicates removed  
  - (optional export: `scout_outliers_handled_final.csv`)

---

## ▶️ How to Run

### 1) Create environment
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows
```

### 2) Install packages
```bash
pip install -U pip
pip install pandas numpy matplotlib seaborn scipy scikit-learn ipywidgets termcolor
```

### 3) Add the raw data
Place the raw JSON file here:
```text
data/as24_cars.json
```

### 4) Run notebooks in order
1) Phase 1 → exports `clean_scout2022.csv`  
2) Phase 2 → exports `filled_scout2022.csv`  
3) Phase 3 → outlier handling + correlation check + duplicate removal (**end**)

---

## 🧠 Key Design Decisions
- ✅ **Fix group keys first** (`model`, `make_model`, `body_type`) → stronger filling + cleaner segments.
- ✅ **Use the right imputation method for the job:**
  - mode for categorical,
  - median for skewed numeric,
  - mean for stable segment averages,
  - ffill/bfill only inside meaningful groups.
- ✅ **Outlier handling is two-layered:**
  1) domain knowledge rules,
  2) robust statistical rules (IQR / z-score).
- ✅ Prefer **“NaN then fill”** when the value is likely a data error but the row is still valuable.
- ✅ Drop rows only when values are clearly unreliable and harm dataset quality.
- ✅ Remove duplicates at the end to prevent repeated records from influencing analysis/modeling.

---

## ⚠️ Limitations
- Thresholds are dataset-specific and based on the segment focus in this project.
- Some extreme cars may be real (luxury/collector vehicles) but can still be removed by IQR/z-score.
- The final CSV export is optional (add `to_csv(...)` in Phase 3 if needed).

---

## 🚀 Next Steps (Optional)
If you continue after this pipeline, typical next steps are:
- encoding categorical features (one-hot / label encoding),
- scaling numeric features,
- training baseline models and evaluating performance.

(These are intentionally out of scope for the current project version.)


