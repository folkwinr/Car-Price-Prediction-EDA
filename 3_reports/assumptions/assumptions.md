# ✅ Assumptions — Part 01: Data Cleaning (AutoScout24)

These assumptions explain what we **accepted as true** while cleaning the raw dataset in Part-01, and why our cleaning choices make sense.

---

## 1) Data Source and Scope
- The input file `as24_cars.json` contains **car listing data** (each row is one listing).
- The dataset is a snapshot from a specific time period; values may change later, but Part-01 focuses on cleaning the snapshot.
- We do **not** try to confirm listing truth (example: if mileage is real). We only make the data usable for analysis.

---

## 2) Schema (Column Names) Assumptions
- Raw column names can contain:
  - spaces, special characters, and `\n` newline characters
- After renaming to **snake_case**, we assume:
  - each column name is unique
  - column names are stable for later steps (Part-02 and Part-03)

---

## 3) Missing Values Assumptions (Part-01 Level)
- Missing values are normal in listing data because sellers do not fill all fields.
- If a column has **very high missing rate** (example rule: **>80%**), we assume:
  - it has low value for this phase, OR
  - it is too hard to fill correctly in Part-02 because there is not enough data
- We accept that some columns are missing because they are **not relevant** for many cars:
  - EV-only fields (battery, range)
  - WLTP-only fields
- In Part-01, we do not try to fill missing values (that is Part-02).  
  Part-01 only drops the “extreme missing” columns and keeps the rest.

---

## 4) Row Meaning Assumptions
- One row represents **one listing**, not always one unique car.
- Duplicate-like rows may exist (same car posted more than once).
- In Part-01, we check duplicates, but we may not always drop them immediately.
  - final duplicate rules can be applied later if needed.

---

## 5) Data Types and Parsing Assumptions
- Many numeric fields are stored as **text** (strings) in the raw dataset.
- We assume it is acceptable to extract numbers from text using parsing:
  - price, mileage, engine size, emissions, weight, etc.
- If parsing fails, we assume:
  - the result becomes missing (NaN)
  - missing will be handled later in Part-02

---

## 6) List-Type Columns Assumptions
- Some columns contain **lists** instead of single values (common in scraped data).
- We assume that for most “single-value” fields stored as lists:
  - the list usually has **one item**
  - taking the **first element** is safe for Part-01
- For the 4 equipment group columns (comfort/media/safety/extras), we assume:
  - they are list-like and can be joined into a readable string for EDA

**Important note:**
- If a list contains multiple items and we use `.explode()`, row counts can change.
- Part-01 assumes lists are mostly single-item where explode is used; otherwise, we prefer a safer method (first element).

---

## 7) Feature Engineering Assumptions (Part-01 Only)
- We assume it is better to create stronger features early:
  - `first_registration` → `age`
  - `power` → `power_kW` and `power_hp`
  - `fuel_consumption` → `cons_avg`, `cons_city`, `cons_country`
- After creating these features, we assume it is acceptable to drop the original source columns because:
  - they become redundant
  - the new features are cleaner and easier to use

---

## 8) Category Simplification Assumptions
- Raw categorical values can have many different labels for the same meaning.
- We assume it is helpful to group similar values into fewer categories, for example:
  - fuel type mapping (many labels → fewer groups)
  - emission/efficiency grouping (where used)
- This is done to make analysis clearer and reduce noise.

---

## 9) Dropping Columns Assumptions
We assume it is correct to drop columns in Part-01 when:
- they are free text and not used (example: `desc`)
- they act like an ID and can cause leakage (example: `offer_number`)
- they are extremely missing (>80%)
- they are redundant after feature engineering (power, fuel_consumption, first_registration)

---

## 10) Output Assumptions (What “clean” means here)
At the end of Part-01, we assume the dataset is “clean enough” when:
- column names are standardized (snake_case)
- key numeric columns are numeric
- core features for later steps exist (age, power split, consumption split)
- extreme-missing columns are removed
- the dataset is ready for:
  - Part-02: filling missing values
  - Part-03: outlier handling
