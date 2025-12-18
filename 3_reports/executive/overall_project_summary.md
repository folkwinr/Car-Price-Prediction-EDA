# ✅ Full Executive Summary (Phase 1 → Phase 3) — AutoScout24 Car Listings Data Preparation

## Project Overview
This project builds a complete **data preparation pipeline** for real-world car listing data (AutoScout24-style). The raw dataset contains typical issues of scraped marketplaces: messy formats, mixed data types, missing values, list-like fields, and extreme values.  
Our goal was to transform the raw data into a **clean, consistent, and analysis-ready dataset** by applying a structured 3-phase process:

- **Phase 1:** Data Cleaning  
- **Phase 2:** Handling Missing Values  
- **Phase 3:** Handling Outliers + Final Sanity Checks (**end of project**)

> 📌 Scope note: The project finishes after the **Phase 3 Final Step** (outliers handled + correlation check + duplicates removed).  
> We do not include additional business questions, inferential statistics, or encoding in the final pipeline.

---

## Why This Pipeline Matters
A car listing dataset looks “simple” at first (price, mileage, fuel type), but the real challenge is data quality:
- many numeric values come as text,
- important columns contain missing values,
- some columns contain lists or inconsistent categories,
- outliers can heavily distort analysis and modeling.

This pipeline makes the dataset reliable by applying:
- consistent cleaning rules,
- explainable missing-value methods,
- robust outlier handling with domain logic,
- final quality checks to reduce noise.

---

## Phase 1 — Data Cleaning (Raw → Clean Baseline)
**Input:** `as24_cars.json`  
**Output:** `clean_scout2022.csv`

### What we did
Phase 1 focused on turning raw JSON into a stable tabular structure:

- **Schema standardization:** renamed columns to consistent `snake_case`, cleaned newline/special-character column names.
- **Type and format cleanup:** transformed numeric-like text into real numeric columns (example: `price`, `mileage`, `engine_size`, `co_emissions`, `empty_weight`).
- **List handling:** managed list-type fields safely (choosing first item when needed, joining list values in equipment columns for readability).
- **Early feature engineering:** created strong, model-friendly features from complex fields:
  - `age` (from first registration)
  - `power_kW` / `power_hp` (from mixed power text)
  - `cons_avg` / `cons_city` / `cons_country` (from fuel consumption field)
- **Noise reduction:** removed high-missing or low-value columns, ID-like fields, and free text not used in this phase.

### Result of Phase 1
We produced a clean baseline dataset with consistent column names and correct data types, ready for systematic missing-value handling.

---

## Phase 2 — Handling Missing Values (Clean → Filled Dataset)
**Input:** `clean_scout2022.csv`  
**Output:** `filled_scout2022.csv`

### Main strategy
Phase 2 did not fill missing values randomly. Instead, it used **segment-based imputation**:
> “Cars with the same model and body type tend to share stable technical properties.”

### What we did
- **Fixed the group keys first** (foundation for correct filling):
  - repaired missing `model` by extracting it from `short_description` using regex,
  - rebuilt `make_model = make + model`,
  - standardized text formatting (Title Case) for consistent grouping.
- **Used method selection based on data type:**
  - **Mode** for categorical columns (gearbox, drivetrain, doors, fuel_type, seats, etc.)
  - **Median** for skewed numeric columns (co_emissions, cons_avg)
  - **Mean** for mileage inside strong segments (`make_model + age`)
  - **ffill/bfill inside groups** for propagation-like fields (previous_owner, upholstery)
- **Applied domain rules for Electric vehicles:**
  - treated Electric cars separately where behavior differs (co_emissions, cons_avg).
- **Feature engineering during missing-value work:**
  - converted long equipment text columns into structured package features:
    - `comfort_convenience_Package`
    - `entertainment_media_Package`
    - `safety_security_Package`
  - dropped raw long-text columns after creating cleaner features.
- **Dropped redundant/low-value columns** to keep the dataset focused (example: dropping `power_hp` after keeping `power_kW`).

### Result of Phase 2
We produced a filled dataset where missing values are reduced using explainable logic, group consistency is improved, and equipment information is simplified into strong package features.

---

## Phase 3 — Handling Outliers + Final Step (Filled → Final Clean Dataset)
**Input:** `filled_scout2022.csv`  
**Output:** Final DataFrame (project ends after final checks)

### Main strategy
Outliers were handled using a combined approach:
- **Domain rules** for clearly impossible values,
- **Robust statistical rules** for heavy-tailed distributions:
  - Tukey’s Fence (IQR)
  - z-score style filtering

### What we did
- **Price outliers:** removed obvious anomaly cases (extreme prices for specific models), then applied IQR-based filtering.
- **Mileage outliers:** removed mileage above realistic thresholds (example: > 1,000,000), then applied IQR filtering.
- **Technical outliers:** for fields like engine size, gears, weight, emissions, and consumption:
  - we often converted extreme values to `NaN`,
  - then filled them using segment-based logic (mode/median),
  - finally applied z-score filtering for the most extreme cases.
- **Dropped low-value or unstable columns:** in this phase, `doors` and `seats` were removed.
- **Final sanity checks (end of project):**
  - checked correlations to understand strong relationships,
  - removed duplicates with `drop_duplicates()` to reduce repeated listings.

### Result of Phase 3
We produced a final dataset where extreme noise is reduced, numeric distributions are more stable, and duplicates are removed—making the dataset reliable for downstream analysis or modeling.

---

## Final Deliverables
This project produces these key outputs:
- **`clean_scout2022.csv`** (after Phase 1)
- **`filled_scout2022.csv`** (after Phase 2)
- **Final DataFrame after Phase 3** (outliers handled + correlation check + duplicates removed)

(Optional: export final DataFrame as a CSV if desired.)

---

## Key Strengths of This Work
- ✅ Clear 3-phase pipeline with strong logic and separation of responsibilities.
- ✅ Missing values handled with **segment-aware** and **explainable** rules.
- ✅ Outlier strategy combines **domain knowledge** and **robust statistics**.
- ✅ Feature engineering improves usability (packages, age, consumption, power splits).
- ✅ Final checks (duplicates + correlation awareness) reduce noise.

---

## Final Note
This pipeline is designed as a professional “data preparation foundation” for any future steps like modeling or dashboards. The dataset produced at the end of Phase 3 is clean, consistent, and stable enough to support advanced analytics with much lower risk of misleading results.
