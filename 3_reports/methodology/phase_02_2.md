# 🧪 Part-02 Methodology — Handling Missing Values (AutoScout24)
This methodology explains **what we thought + what we did**, in a clear **step-by-step** way, including **decision rules**, **why we used specific code**, and **when we used feature engineering** instead of simple filling.

> **Goal of Part-02:**  
> Turn the **cleaned but incomplete** dataset into a **fully usable dataset** by handling missing values with **smart, realistic rules** (not random filling).  
> Output is ready for **Part-03 (Outliers)**.

---

## 🧭 0) Core Idea: Missing values are not random
We assumed missingness happens for real reasons in listings:
- sellers skip fields
- some fields exist only for specific car types (EV/WLTP)
- some values are hidden inside other text (like model inside description)

So we did **not** use “one method for all columns”.
Instead, we built a **decision tree** and used different paths:
- **group-based mode** for stable categorical/mostly-constant fields
- **group-based median/mean** for numeric fields with variation
- **ffill/bfill inside groups** when patterns repeat within groups
- **regex extraction** when the value exists in another column
- **feature engineering** when the raw field is too complex and not model-friendly

---

## 1) 🧰 Setup & Visibility (Before filling, we made the problem clear)

### 1.1 Load + protect
- We loaded: `clean_scout2022.csv`
- We kept the process reproducible (no changes to raw Part-01 file).

### 1.2 Quick overview tools (why we used them)
We used quick diagnostics (example: **skimpy**) + our helper checks:
- **Why skimpy?**  
  It gives a fast view of:
  - which columns are numeric/categorical
  - missing rates
  - extreme values quickly
- **Why our functions?**  
  We needed targeted control per column:
  - `first_looking(col)` → missing %, unique values, value_counts
  - `df_nans()` / `show_missing_values()` → missing ranking

**Decision after visibility**
- If a column is missing a lot but still important → we fill it
- If a column is missing a little but is a key for grouping → we fix it first

---

## 2) ✅ Priority Rule: Fix “group keys” first (otherwise all filling becomes wrong)
### Why this matters
Most of our filling is **group-based**.  
If `model` or `make_model` is wrong/missing, then:
- groupby statistics are wrong
- filled values become unreliable

So our first thinking was:
> “Before filling anything else, make sure grouping columns are correct.”

---

## 3) 🔧 Step-by-step Missing Handling Strategy (Decision Tree)

### Step 1 — Identify missing columns and categorize them
For each column with missing values, we asked:
1) Is it **categorical** or **numeric**?
2) Is it **stable inside a group** (same for a model/body type), or does it vary a lot?
3) Is missing caused by:
   - real absence (not applicable),
   - formatting (`"-"`),
   - or value hidden in another column (text)?

Then we chose the method below.

---

## 4) 🧩 Method A — Regex Extraction (Use another column to recover missing values)
### When we used it
If a value is missing in a column but likely appears in another text field.

### Case: `model` missing
**What we saw**
- `model` missing breaks `make_model` quality and group fills.
- But `short_description` often contains the model as text.

**What we did**
1) Built a strong regex (`model_pattern`) that matches common model names.
2) Extracted candidates:
   - `extracted_models = short_description.str.extract(...).bfill(axis=1)[0]`
3) Filled:
   - `model.fillna(extracted_models, inplace=True)`

**Why this code**
- `str.extract()` lets us pull structured info from unstructured text.
- `bfill(axis=1)` helps when multiple regex capture groups exist.

**Decision rule**
- If `model` is still missing after extraction → inspect the rows.
- If we cannot confidently recover → **drop the row**.
  - Reason: wrong model = wrong grouping = wrong filling everywhere.

✅ Result:
- We dropped a small number of rows (6) to keep dataset quality high.

---

## 5) 🧩 Method B — Standard “Fill Engine” with Hierarchy (Our main pipeline)
To avoid rewriting code for every column, we created reusable functions:
- `fill(...)` for mode/mean/median/ffill with fallbacks
- `fill_mode(...)` specialized for hierarchical mode
- `fill_median(...)` specialized for multi-level median
- `fill_prop(...)` for ffill/bfill propagation inside a group

### Why we used hierarchy (fallback logic)
One group might be too small or fully missing.
So we used this logic:

✅ Primary fill (most specific):
- `(group1 + group2)`  
⬇️ if still missing  
✅ Secondary fill:
- `(group1)`  
⬇️ if still missing  
✅ Final fallback:
- global statistic (mode/median/mean)

This makes filling more robust and reduces “random” wrong fills.

---

## 6) 🧩 Method C — Mode filling (best for stable categorical fields)
### When we chose mode
We used **mode** when:
- the column is categorical, OR
- numeric but usually constant inside a model/segment (example: doors)

### Examples (what we thought → what we did)
- **doors**: stable by `make_model + body_type` → fill with mode
- **gearbox**: stable by segment → fill with mode
- **drivetrain**: stable by segment → fill with mode
- **power_kW**: stable by model/body type → fill with mode
- **seats**: stable by model/body type → fill with mode

**Why not mean/median here?**
- For categorical labels, mean/median is not valid.
- For “fixed spec” numbers, mode often gives the correct factory spec.

---

## 7) 🧩 Method D — Median / Mean filling (best for numeric fields with variation)
### When we chose median/mean
We used median/mean when:
- values vary within a group
- we want to reduce outlier influence (median is stronger)

### Example: `co_emissions`
**What we saw**
- Many missing values.
- Electric cars behave differently (special case).

**What we did**
1) **Special-case rule for Electric**
   - We checked Electric distribution and filled Electric missing using Electric-specific logic (mode-like behavior).
2) **General numeric fill**
   - `fill_median(df, "make_model", "body_type", "fuel_type", "co_emissions")`

**Why median**
- Emissions can have real extremes.
- Median is safer than mean when data has skew.

### Example: `mileage`
**What we saw**
- Mileage depends strongly on `age` and `make_model`.

**What we did**
- Filled missing using grouped **mean**:
  - `groupby(["make_model","age"]).mileage.transform("mean")`

**Why mean here**
- Mileage is continuous and mean works well when group is meaningful (`make_model + age`).

---

## 8) 🧩 Method E — ffill/bfill inside groups (propagation)
### When we used ffill/bfill
We used it when:
- the column values repeat inside a group
- and the dataset has enough repeated records

### Examples
- `previous_owner`:
  - filled within `age` group via `fill_prop(age, previous_owner)`
- `upholstery`:
  - filled via `fill(..., method="ffill")` within `make_model + body_type`

**Why not mode here?**
- Some text categories can be messy and repeated; propagation in a stable group can work well.
- Also useful when mode is weak due to many categories.

**Important reasoning**
- We applied propagation **inside groups**, not globally, to avoid random spreads.

---

## 9) 🧠 Special Rules (Domain Knowledge Overrides)
Some columns need domain logic, not pure statistics.

### Rule 1: `age` with low mileage
**What we saw**
- A few cases had missing age but mileage was very low.

**What we did**
- If `mileage < 10000` and age missing → set `age = 0`

**Why**
- A car with very low mileage is likely new; this is a practical listing assumption.

### Rule 2: Electric consumption
**What we saw**
- EVs don’t follow classic fuel consumption patterns.

**What we did**
- For `fuel_type == "Electric"` we set a domain constant for `cons_avg` (as used in the notebook).

---

## 10) 🧠 Feature Engineering inside Part-02 (We did more than filling)
Sometimes filling the raw column is not enough; the raw format is not model-friendly.

### Why we did feature engineering here
- Equipment columns are long text/list-like.
- They are hard for models and create noise.
- Better: convert them into simple “package levels”.

### What we did
1) Filled missing in the raw equipment column using mode:
   - `fill(df, "make_model", "body_type", equipment_col, "mode")`
2) Built package features using keyword rules:
   - `comfort_convenience_Package`
   - `entertainment_media_Package`
   - `safety_security_Package`
3) Dropped the original raw equipment columns:
   - less noise, simpler model input

**Reason**
- This creates high-signal features and reduces dimensional complexity.

---

## 11) 🗑️ Drop Decisions in Part-02 (Not random — reasons are clear)
We dropped columns when:
1) They are helper-only:
   - `extracted_models`, `modified_make_model`, `short_description`
2) They are redundant:
   - `power_hp` redundant with `power_kW`
3) They are low-value compared to stronger related features:
   - `cylinders` after we already have engine_size + power_kW

We dropped rows when:
- `model` could not be recovered safely (small count, high impact)

---

## 12) ✅ Final Quality Gates (How we validated the result)
After filling, we checked:
- missing rates are reduced (critical columns improved)
- group keys (`make_model`, `model`, `body_type`) are consistent
- filled numeric columns look reasonable using `.describe()` and group summaries
- the final dataset shape is stable and ready for Part-03

---

## 🏁 Output of Part-02
- Final dataset saved as: `filled_scout2022.csv`
- Final columns: 30
- Dataset is ready for:
  - Outlier handling (Part-03)
  - Modeling / EDA with fewer missing issues