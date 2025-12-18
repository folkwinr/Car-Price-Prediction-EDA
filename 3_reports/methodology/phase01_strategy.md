# 🧪 Part-01 Methodology (Data Cleaning) — Step-by-Step (AutoScout24)

> In this part, our goal was: **raw JSON → a clean, consistent, analysis/model-ready table**.  
> Our strategy was: **general cleaning + quality checks first**, then **column-by-column cleaning**, then **feature engineering**, and finally **final checks**.

---

## 🧭 0) Starting Logic: What problem are we solving?
Raw listing data usually has these issues:
- 🧾 messy column names / newline characters / special symbols (schema noise)
- 🔢 numeric values stored as **text** (price, mileage, consumption, power…)
- 🧩 some cells are **lists** (equipment groups, some categorical fields)
- 🕳️ many missing values (especially WLTP / EV fields)
- 🔁 possible duplicates (common in scraped data)

So our decision process was always:
- **First visibility:** “What do we have, how missing is it, what is the format?”
- **Then cleaning:** “schema + noise removal + type conversion”
- **Then meaning:** “feature engineering + category simplification”
- **Finally checks:** “data quality gates”

---

## 1) 🧰 General Setup
### 1.1 📥 Load + Copy (Protect raw data)
- ✅ We loaded raw JSON using `pd.read_json(...)`.
- ✅ We created a copy: `df = df0.copy()`.
- **Why?** To keep the raw dataset safe and make it easy to compare changes.

### 1.2 🔍 Quick overview (skimpy + fast EDA tools)
- ✅ We used **skimpy** (and similar quick summaries) to see:
  - column types
  - missing rates
  - basic distribution signals
  quickly.
- ✅ We also used our helper functions (example: `first_looking`) to check per column:
  - missing percent / missing count
  - number of unique values
  - value_counts

**Main idea:**
> “See the problem first. If you transform before understanding formats, parsing errors can grow.”

---

## 2) 🧹 Global Cleaning Rules
### 2.1 🏷️ Column name standardization (Schema normalize)
- ✅ We used `to_snake_case()` to standardize column names:
  - remove newline characters / spaces / special symbols
  - lowercase + underscores
- **Why?** Safer code, better readability, better GitHub quality.

### 2.2 🗑️ Drop fully empty rows
- ✅ `dropna(how="all")`
- **Why?** Rows with no information only add noise.

### 2.3 🕳️ Remove very empty columns (Missing threshold)
- ✅ We checked missing rates (`df_nans` / `show_missing_values`).
- ✅ Rule: **if a column has >80% missing values → drop it**
- **Why?**
  - even in Part-02, there is not enough data to fill it well
  - these columns make the dataset bigger but not better

> Decision point:
> - If **>80% missing** → **drop**
> - If medium missing → keep and handle in **Part-02**
> - If a **core** column (price/mileage) → keep and fill later

### 2.4 🔁 Duplicate check
- ✅ We tried `duplicated()` checks.
- 🧩 Because list-type columns can cause issues, we used a workaround like:
  - `df.astype(str).duplicated()` for a practical check
- **Why?** Scraped data can include repeated listings or near-repeats.

---

## 3) 🧩 Column-by-Column Cleaning Strategy
For each column we asked these 3 questions:

### ✅ Question-1: What is the column format?
- If it is a **list** → list handling
- If it is **numeric-like text** → regex + numeric conversion
- If it is **category/text** → strip/normalize/mapping
- If it is **free text (desc)** → drop in this phase (NLP not in scope)

### ✅ Question-2: Is this column useful?
- Is it a core feature? (price, mileage, age, power, fuel…)
- Is it too missing?
- Is it an ID / leakage risk? (Offer number)

### ✅ Question-3: Can we create a better feature from it?
- power → kW + hp
- fuel_consumption → avg/city/country
- first_registration → age

---

## 4) 🧷 List Handling (Decision tree for list-type cells)
Some columns came as **lists**.

### 4.1 ✅ If the list is usually single-item (most common case)
- We used:
  - `x[0] if isinstance(x, list) else x`
- **Why?** It converts to a single value without changing row count.

### 4.2 ⚠️ Where we used `.explode()` (practical but risky)
- For some columns we used: `explode().str.strip(...)`.
- **When is it OK?**
  - when we believe lists are almost always single-item
- **Risk:**
  - if a list has >1 item, `explode()` increases the number of rows → dataset can break

> Strategy:
> - If we are “confident” → explode  
> - If we are “not sure” → take the first element (safer)

### 4.3 🧩 Equipment columns: list → readable text
- For equipment groups (`comfort`, `entertainment`, `safety`, `extras`):
  - we used `", ".join(list)` to make one readable string
- **Why?** Part-01 aims for **readability + stable dataset**
- **Note:** For modeling later, better options are:
  - `equipment_count`
  - `has_feature_X` (0/1 flags)

---

## 5) 🔡 Regex for Numeric Conversion (Text → Numeric Parsing)
This was the “core engine” of Part-01.

### 5.1 💰 Price
- We saw: values are text with currency and separators.
- We applied:
  - regex to extract the number (`extract`)
  - remove separators (like `,`)
  - convert to numeric (`astype(float)`)

**Why?** Without numeric price, EDA/outliers/models are not possible.

### 5.2 🛣️ Mileage
- We saw: “km” text and separators.
- We applied:
  - separator cleanup
  - regex digit extraction
  - numeric conversion

### 5.3 ⚙️ Engine/weight/gear/cylinders-like fields
- We saw: numeric-like strings.
- We applied:
  - `extract('(\d+)')`
  - numeric conversion

> General rule:
> - if a number is inside text → extract it → convert to numeric  
> - if parsing is not safe → treat it as missing and handle in Part-02

---

## 6) 🧠 Feature Engineering — “Clean + Make it stronger”
This part was not only cleaning, but also making the data more useful.

### 6.1 📅 First registration → Age
- We saw: registration format can be mixed, and **age** is easier for analysis.
- We applied:
  - extract year (often last 4 characters)
  - `age = reference_year - year`
- Then:
  - we dropped source columns like `first_registration` and `production_date` (redundant)

### 6.2 ⚙️ Power → power_kW + power_hp
- We saw: power text often contains both kW and hp.
- We applied:
  - if list → take first element
  - regex to extract two numbers
  - created two numeric columns
- Then:
  - dropped the source `power` column

### 6.3 ⛽ Fuel consumption → cons_avg / cons_city / cons_country
- We saw: consumption is a complex field in a single column.
- We applied:
  - helper functions to select correct parts
  - regex numeric extraction
  - created `cons_avg`, `cons_city`, `cons_country`
- Then:
  - dropped the source `fuel_consumption` column

---

## 7) 🧩 Categorical Normalization (Simplifying categories)
### 7.1 ⛽ Fuel type mapping
- We saw: many different fuel labels.
- We applied:
  - split by `/` (take the first part)
  - mapping function to group similar labels
- **Why?** Too many categories makes analysis messy; fewer groups are clearer.

### 7.2 🌿 Emission / Efficiency grouping
- We saw: many variants in emission/efficiency labels.
- We applied:
  - functions that normalize/group values
- Decision:
  - some of these columns were later dropped (not needed for this phase)

---

## 8) 🗑️ Drop Strategy (What we removed and why)
### 8.1 🧾 Free text
- long text like `desc`:
  - dropped (NLP not included in this phase)

### 8.2 🆔 ID / leakage
- `offer_number`:
  - dropped to avoid memorization/leakage in models

### 8.3 🕳️ Very missing columns
- many WLTP/EV fields:
  - dropped by the >80% missing rule

### 8.4 🔁 Redundant after feature engineering
- `power` dropped after creating `power_kW/hp`
- `fuel_consumption` dropped after creating `cons_*`
- `first_registration` dropped after creating `age`

---

## 9) ✅ Data Quality Gates (Final checks)
At the end of Part-01 we checked:
- 🧪 column dtypes (numeric fields are numeric)
- 🕳️ missing report (ready for Part-02)
- 🔁 duplicate check output (drop decision can be applied later)
- 📌 basic logic checks (negative values noted for Part-03 outlier handling)

---

## 🏁 Output: What we have after Part-01
- ✅ clean, standardized column names (snake_case)
- ✅ core numeric columns ready for analysis:
  - price, mileage, age, power_kW/hp, cons_*
- ✅ equipment columns made readable
- ✅ very missing / low-value / ID columns removed
- ✅ strong base for Part-02 (missing) and Part-03 (outliers)

---

## 🔥 Mini Decision Log (Short)
- **Missing >80%** → drop  
- **List field** → (if confident) explode, (if not) first element  
- **Text-number** → regex extract + numeric conversion  
- **Better feature possible** → create feature, then drop source column  
- **Free text / ID** → drop (in this phase)
