# ✅ Part-02 Executive Summary (Handling Missing Values)

## Project Context
Part-02 is the second stage of our AutoScout24 car listing project.  
Part-01 focused on cleaning the raw data (types, formats, noisy columns). After that, the dataset was cleaner, but many important columns still had missing values. In this part, we handled missing values in a structured way, so the dataset becomes reliable for analysis and ready for Part-03 (Outlier Handling).

**Input:** `clean_scout2022.csv`  
**Output:** `filled_scout2022.csv`

---

## Main Objective
Our goal was not only to “fill empty cells”, but to do it in a way that keeps the data realistic and consistent.

We aimed to:
- improve key identity columns used for grouping,
- fill missing values using context (not random values),
- apply domain rules where needed (especially for Electric cars),
- create cleaner, model-friendly features from noisy text columns.

---

## Core Strategy (How we approached missing values)
### 1) Fix the “group keys” first
Most of our filling methods depend on grouping, so we first made sure the main grouping columns were correct:
- `model`
- `make_model`
- `body_type`

If these columns are wrong or missing, any group-based filling becomes weak and can create wrong values. So we treated them as the foundation.

---

## Key Work Done (What we actually did)

### ✅ A) Repair `model` using `short_description`
Some records had a missing `model`. Instead of filling it with a generic value, we tried to recover the real model name.

We did this by:
- using a regex pattern to extract the model from `short_description`,
- filling missing `model` values with that extracted result,
- checking what remained missing after extraction,
- dropping a very small number of rows where the model still could not be recovered.

This was a high-impact step because many other columns were filled using groups that include model information.

---

### ✅ B) Rebuild and standardize `make_model`
After `model` was corrected, we rebuilt `make_model` using:
- `make + model`

Then we:
- standardized the text format (Title Case),
- applied a few targeted text fixes for inconsistent naming.

This improved grouping quality and reduced “same car but different text” issues.

---

### ✅ C) Use group-based filling with fallback (the main engine)
Instead of one global value, we filled missing values using a hierarchy:

1) **Most specific group** (example: `make_model + body_type`)  
2) **Less specific group** (example: `make_model`)  
3) **Global fallback** (whole dataset)

This approach is strong because many car attributes are stable inside a segment.

---

## Imputation Methods (Why we used different techniques)
We did not use one filling method for all columns. We selected the method based on column type and behavior:

### 🧩 Mode (most frequent value) for categorical columns
Used for columns like:
- `doors`, `gearbox`, `fuel_type`, `drivetrain`, `seats`, and often `engine_size` (stable inside segments)

**Reason:** In a stable segment, the most common value is usually correct.

---

### 🔢 Median for numeric columns with potential skew
Used for:
- `co_emissions`
- `cons_avg`

**Reason:** These columns can contain extreme values, and median is more robust than mean.

We used multi-level grouping (more specific → less specific → global median).

---

### 📈 Mean for mileage in strong segment groups
Used for:
- `mileage` grouped by `make_model + age`

**Reason:** Mileage tends to follow an average pattern inside similar cars with similar age.

---

### 🔁 ffill/bfill inside groups for “propagation-like” fields
Used for:
- `previous_owner` (within `age`)
- `upholstery` (within `make_model + body_type`, after category cleanup)

**Reason:** These fields are often repeated inside a group, so propagation can work well when grouping is correct.

---

## Domain Rules (Where we did not trust generic filling)
### ⚡ Electric vehicles
Electric cars behave differently from fuel cars, so we applied special logic:

- For `co_emissions`: Electric cars often have near-zero values, so we handled Electric rows separately first.
- For `cons_avg`: We set a specific value for Electric cars (a domain-based constant) to avoid mixing electric behavior with fuel-car patterns.

This reduced the risk of “fuel-car-like” imputations in Electric rows.

---

## Feature Engineering in Part-02 (Not only filling)
We also improved the dataset by simplifying complex equipment columns.

### ✅ Equipment text → Package features
For long text equipment columns:
- `comfort_convenience`
- `entertainment_media`
- `safety_security`

We:
1) filled missing values so the text is consistent,
2) created package-level features based on keyword rules:
   - `comfort_convenience_Package`
   - `entertainment_media_Package`
   - `safety_security_Package`
3) dropped the original long-text columns to reduce noise and make the dataset easier to model.

This turned messy text into structured information.

---

## Drop Decisions (What we removed and why)
We dropped columns for clear reasons:
- helper columns used only during repair (example: extracted model columns),
- redundant columns (example: `power_hp` after keeping `power_kW`),
- less useful consumption sub-columns (`cons_city`, `cons_country`) after choosing `cons_avg`,
- low-value columns like `cylinders` (after filling) to keep the dataset focused.

---

## Final Outcome (What we achieved)
By the end of Part-02:
- the dataset had much fewer missing values in key columns,
- group keys became cleaner and more reliable,
- Electric cars were treated with correct logic,
- equipment information became structured package features,
- the output dataset became ready for Part-03 (outlier handling) and later modeling.

**Final output file:** `filled_scout2022.csv`
