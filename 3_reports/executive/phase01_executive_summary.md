# Executive Summary — Part 01: Data Cleaning (AutoScout24 Cars)

## 1) Purpose and Value
Part 01 prepares the AutoScout24 car listings dataset for the next steps:
- **Part 02: Filling Missing Values**
- **Part 03: Outlier Handling**

The goal is clear: **turn raw JSON data into a clean, consistent, and usable table** for analysis and later modeling.

This step is important because raw listing data often has:
- messy column names
- numbers saved as text
- list-type fields (not single values)
- many missing values
- different formats for the same type of data

Part 01 reduces these problems and creates a strong base dataset.

---

## 2) Input and Output

### Input
- `as24_cars.json` (raw listings data in JSON format)

### Output
- A cleaned DataFrame (clean dataset)

Recommended saved file for the pipeline:
- `data/processed/phase01_clean.parquet` (or `.csv`)

This output is the main input for Part 02 and Part 03.

---

## 3) Main Approach (How we worked)
We follow a simple order:

### A) First: Fix the structure (schema)
- Make column names clean and standard.
- Make the dataset easier to read and safer to use in code.

### B) Then: Reduce noise
- Remove fully empty rows.
- Remove columns with very high missing rate (example rule: **more than 80% missing**).

### C) Finally: Make key columns usable
- Convert important columns to the correct data types (numeric when needed).
- Create useful features like **age** and split complex fields into clear parts.

---

## 4) What We Changed (Key Cleaning Work)

### 4.1 Load and protect the raw data
- Load the JSON file into pandas.
- Create a copy so the original raw dataset stays unchanged.
- This helps if we need to check or restart the process.

---

### 4.2 Column name cleaning (standard names)
Raw data can have:
- spaces
- symbols
- multi-line column headers
- mixed naming styles

We standardize column names into **snake_case**, for example:
- `First Registration` → `first_registration`
- `Fuel Consumption` → `fuel_consumption`

This makes code cleaner and reduces mistakes.

---

### 4.3 Remove very weak columns and empty rows
We remove:
- rows that are completely empty (`dropna(how="all")`)
- columns with very high missing values (example threshold: **>80% missing**)

**Reason:** columns with too many missing values usually add noise and do not help much in early analysis.

---

## 5) Key Column Transformations (Most Important Results)

### 💰 Price
**Problem:** price is often stored as text with separators and symbols.  
**Action:** parse it and convert to numeric.

**Result:** `price` becomes ready for:
- summary statistics
- plots
- later outlier checks
- modeling

---

### 🛣️ Mileage
**Problem:** mileage may be stored as text with commas, dots, or extra text.  
**Action:** clean separators and extract the number, then convert to numeric.

**Result:** `mileage` becomes usable for comparisons and relationships like:
- mileage vs price
- mileage vs age

---

### 📅 First Registration → Age
**Problem:** dates/years come in different formats, and year is not always easy to use.  
**Action:** extract the year and create **age**:

- `age = reference_year - first_registration_year`

**Result:** `age` is a clean numeric feature and often works better than the raw date.

**Important note:** if the reference year is fixed in code (example: 2022), it should later be moved to a config setting (so it stays correct).

---

### ⚙️ Power → power_kW and power_hp
**Problem:** power may be mixed text and can include both kW and hp.  
**Action:** parse the text and split it into two numeric columns:
- `power_kw`
- `power_hp`

**Result:** we keep more information and make power easy to use in analysis.

---

### ⛽ Fuel Consumption → clear columns (consumption parts)
**Problem:** fuel consumption may come as a complex field (sometimes nested, sometimes mixed text).  
**Action:** extract numeric values and split into separate columns, for example:
- `cons_avg` (average)
- `cons_city` (city)
- `cons_country` (outside city / highway)

**Result:** consumption becomes clear numeric fields and can be used for:
- efficiency comparisons
- price vs efficiency analysis
- outlier checks

---

### 🧩 Equipment / feature list columns (comfort, safety, extras)
**Problem:** many equipment columns are lists (not single values).  
**Action (for Part 01):** convert them into a readable format (for example, join list items into one text string).

**Result:** easier EDA and reporting.

**Note for later:** for modeling, these fields are often better as:
- feature counts (example: `extras_count`)
- 0/1 flags (multi-hot encoding)

---

## 6) Data Quality Checks (What we verified)
After cleaning, we do basic checks to confirm the dataset is stable:

- **Missing report:** missing values by column (counts and rates)
- **Duplicates check:** raw data may have repeated or near-repeated rows
- **Type consistency:** avoid a column having mixed types (example: numbers and strings together)

These checks reduce risk before Part 02 and Part 03.

---

## 7) Main Design Decisions (and why)

### Decision 1: Drop columns with >80% missing values
- These columns usually have too little information.
- Keeping them can add noise and slow down analysis.
- This rule can be adjusted later if a high-missing column still carries strong value.

### Decision 2: Drop very noisy text fields (example: description)
- Free text can be useful, but it needs NLP work.
- In Part 01, we focus on strong structured signals like price, mileage, age, power, and consumption.

### Decision 3: Create strong base features early (age, power split, consumption split)
- These are key drivers for car price and car type.
- They are more useful than raw mixed-format fields.

---

## 8) Ready for Next Steps

### Part 02: Filling Missing Values
After Part 01, we can do missing value work in a clean way:
- numeric fill: median or group median (by make/model/body type)
- categorical fill: mode or "Unknown"
- optional: add missing flags like `price_missing`, `mileage_missing`

### Part 03: Outlier Handling
Now key numeric columns are ready for outlier checks:
- `price`, `mileage`, `age`, `power_kw`, `cons_*`
Possible actions:
- remove impossible values (example: negative price, negative mileage, age < 0)
- cap extreme values (winsorize)
- log transform for heavy-tailed fields (especially price)
- check outliers within groups (example: within `make_model`) for fairness

---

## 9) Final Conclusion
Part 01 turns raw car listing data into a clean and stable dataset.
It standardizes column names, removes heavy noise, converts key fields to numeric types, and creates important features like **age**, **power_kw/power_hp**, and **consumption parts**.

This cleaned dataset is a strong base for:
- Part 02 (missing values)
- Part 03 (outliers)
and for deeper analysis and modeling later.