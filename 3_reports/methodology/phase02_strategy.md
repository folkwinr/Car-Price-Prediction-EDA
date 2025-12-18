# 🧩 Part-02 Methodology (Handling Missing Values) — What We Thought, What We Did (Step-by-Step)

> 🎯 **Goal of Part-02:**  
> Take `clean_scout2022.csv` (already cleaned in Part-01) and produce a dataset where **missing values are handled in a controlled, explainable way**, using:
> - **group-based imputation (grouping + fallback)**
> - **domain rules** (especially Electric cars)
> - **light feature engineering** (turn long equipment text into packages)
>
> ✅ **Input:** `clean_scout2022.csv`  
> ✅ **Output:** `filled_scout2022.csv`

---

## 0) 🧠 Core Idea (The “why” behind everything)
Scraped car listing data is messy, but it is *structured messy*:
- Many values are missing because sellers don’t fill them.
- A lot of variables are *stable* inside a segment:
  - within the same **make_model**, **body_type**, **gearbox**, **fuel_type**, **age**
- So instead of random filling, we used **context-aware filling**:
  - “If I know the model and body type, I can guess doors / engine size / drivetrain much better.”

✅ **Main principle:**  
**Fix the “group keys” first**, then fill the rest using those keys.

---

## 1) 🧰 Setup + Quick Health Check (Before touching missing values)

### 1.1 📥 Load and protect data
- We loaded the cleaned dataset and created a copy so we don’t damage the source.

```python
df0 = pd.read_csv("clean_scout2022.csv")
df  = df0.copy()
```

### 1.2 🔎 Quick baseline checks
We used:
- `df.shape`, `df.info()` to understand types and size
- repeated `first_looking(col)` to see:
  - % missing
  - unique values
  - value_counts (including NaN)

✅ Why this matters:
- We didn’t want to “fill blindly”.  
- We first **measured** each column’s missing and patterns.

---

## 2) 🧱 Step-By-Step Pipeline (Our actual working order)

### ✅ Step 1 — Make grouping keys stable (because everything depends on them)
**Why first?**  
If `model` is missing, then `(make_model + body_type)` groups become weak and imputation becomes wrong.

#### 1A) Repair `model` using `short_description` (regex extraction)
What we did:
- We created a big `model_pattern`
- We extracted models from `short_description`
- We filled missing `model` with extracted results
- If still missing → we inspected remaining rows and **dropped unrecoverable ones**

```python
df["extracted_models"] = (
    df["short_description"].str.extract(model_pattern, flags=re.IGNORECASE)
).bfill(axis=1)[0]

df["model"] = df["model"].fillna(df["extracted_models"])
df.dropna(subset=["model"], inplace=True)  # remove the last unrecoverable records
```

📌 What we observed (from notebook notes):
- `model` had **276 NaNs before**
- after regex fill, **6 rows** still had NaN → we **dropped those 6 rows**

#### 1B) Rebuild `make_model` to be consistent
We assumed `make + model` is a more reliable identity than raw `make_model` when model is fixed.

```python
df["modified_make_model"] = df["make"] + " " + df["model"]
# use it to update make_model
```

Then we standardized formatting:
- `.str.title()` on `make_model`, `make`, `model`, and also `body_type`  
(to remove writing differences like `FORD mustang` vs `Ford Mustang`)

✅ Finally, we removed helper columns:
```python
df.drop(["modified_make_model", "short_description", "extracted_models"], axis=1, inplace=True)
```

---

### ✅ Step 2 — Use a “Missing Pattern Lens” before filling (we don’t fill immediately)
For many columns we used the same technique:

#### 👁️ “Dash trick” (temporary visibility trick)
We temporarily replaced NaN with `"-"` to:
- make missing values visible in `describe()` and `value_counts`
- filter rows with missing quickly (`df[col] == "-"`)

Then we switched back to real missing (`np.nan`) before actual filling.

```python
df[col].fillna("-", inplace=True)   # inspect patterns
# ... explore patterns (groupby, value_counts, describe)
df[col].replace("-", np.nan, inplace=True)  # ready for real fill
```

✅ Why we did this:
- NaN is “invisible” in many text checks.
- Using `"-"` helped us *see* hidden patterns and take correct decisions.

---

### ✅ Step 3 — Choose fill method based on column nature (Decision Rules)
We did **not** use a single method for all columns.

#### 3.1 🧩 If column is categorical (categories/labels) → MODE
Examples:
- `doors`, `gearbox`, `fuel_type`, `drivetrain`, `seats`, `engine_size` *(treated as stable segment value)*

**Reason:**  
Inside `(make_model + body_type)` the most common value is often the correct one.

We used a two-level fallback logic:
1) group by `(group_col1 + group_col2)`
2) fallback to group by `(group_col1)`
3) fallback to global mode

✅ Implemented in our main engine function `fill(..., method="mode")`

```python
fill(df, "make_model", "body_type", "doors", "mode")
fill(df, "make_model", "body_type", "gearbox", "mode")
fill(df, "make_model", "gearbox",   "fuel_type", "mode")
```

#### 3.2 🔢 If column is numeric but can have real outliers → MEDIAN
We preferred median for numeric columns that can be skewed:
- `co_emissions`
- `cons_avg`

**Reason:**  
Mean is sensitive to extreme values; median is more robust.

We used **multi-level median fallback** with `fill_median()`:
1) `(make_model + body_type + fuel_type)`
2) `(make_model + body_type)`
3) `(make_model)`
4) global median

```python
fill_median(df, "make_model", "body_type", "fuel_type", "co_emissions")
fill_median(df, "make_model", "body_type", "fuel_type", "cons_avg")
```

#### 3.3 📈 If column is numeric and strongly tied to a segment average → MEAN
We used mean where it makes sense:
- `mileage` (depending on `make_model` and `age`)

**Reason:**  
Mileage behaves like an average pattern within (model, age) groups.

```python
df["mileage"].fillna(
    df.groupby(["make_model", "age"]).mileage.transform("mean"),
    inplace=True
)
```

#### 3.4 🔁 If column behaves like a “propagated attribute” inside a group → FFILL + BFILL
We used forward/back fill where the value is not “computed”, but often repeated in a structured way inside groups:
- `upholstery` (after category redesign)
- `previous_owner` (within `age` groups)

**Reason:**  
When groups are consistent, ffill/bfill fills gaps smoothly without forcing a global category.

```python
fill(df, "make_model", "body_type", "upholstery", "ffill")
fill_prop(df, "age", "previous_owner")
```

⚠️ Important note:
- We used ffill/bfill **inside groups** first (safer than global ffill directly).

---

## 4) 🧠 Special Rules (Domain Knowledge Overrides)
Some columns cannot be filled correctly without “car logic”.

### 4.1 🧾 Warranty → convert to Yes/No using a rule
We did not try to guess warranty months/years.  
We simplified it into a strong signal.

```python
df["warranty"].fillna("-", inplace=True)

def warrantyclassifier(x):
    return "No" if "-" in x else "Yes"

df["warranty"] = df["warranty"].astype(str).apply(warrantyclassifier)
```

✅ Why this is good:
- Warranty presence is often more useful than exact value.
- Less noise, more model-friendly.

### 4.2 ⚡ Electric cars & `co_emissions`
We checked Electric emissions separately:
- Electric cars should mostly be near **0** emissions.
- So we filled missing emissions for Electric cars using **Electric mode** first.

```python
df["co_emissions"].fillna("-", inplace=True)
df.loc[df["fuel_type"] == "Electric", "co_emissions"] = (
    df.loc[df["fuel_type"] == "Electric", "co_emissions"]
      .replace("-", np.nan)
      .fillna(df.loc[df["fuel_type"] == "Electric", "co_emissions"].mode()[0])
)
```

Then we applied the global 3-level median strategy for all cars.

✅ Why this order:
- Electric cars are a special distribution.  
- If we mix them with fuel cars too early, the fill can become wrong.

### 4.3 ⚡ Electric cars & `cons_avg`
We used a domain constant for Electric consumption:

```python
df.loc[df["fuel_type"] == "Electric", "cons_avg"] = 2.359
```

✅ Why:
- Electric consumption behaves very differently.
- This prevents “fuel-car-like” imputation from corrupting Electric rows.

### 4.4 🪑 Upholstery redesign before filling
We reduced category chaos using domain knowledge:
- “Velour” → “Cloth”
- “alcantara / Part leather / Full leather” → “Part/Full Leather”
- “Other” → NaN (noise category)

Then we filled with group ffill/bfill.

```python
df["upholstery"].replace(
    ["Velour", "alcantara", "Part leather", "Full leather"],
    ["Cloth",  "Part/Full Leather", "Part/Full Leather", "Part/Full Leather"],
    inplace=True
)
df["upholstery"].replace("Other", np.nan, inplace=True)
fill(df, "make_model", "body_type", "upholstery", "ffill")
```

✅ Why this order:
- If we fill first, we propagate messy labels.
- If we standardize first, we propagate clean categories.

### 4.5 🧓 Age rule using mileage (small but smart)
We inspected missing ages and mileage patterns.
If mileage is very low, a missing age likely means **new car**.

```python
df["age"].fillna("-", inplace=True)
cond_age1 = (df["mileage"] < 10000)
df.loc[cond_age1, "age"] = df.loc[cond_age1, "age"].replace("-", 0)
```

✅ Why:
- A very low mileage vehicle often means age ≈ 0 in listing contexts.
- This made age logic more consistent before other grouped fills.

---

## 5) 🧪 Engineering Features during Part-02 (Not only “fill”, also “improve”)
Some raw columns were long text (equipment lists). Instead of keeping them as-is:
- we filled them (so we have stable content)
- then we built **package-level features**
- then we dropped raw long-text columns (less noise)

### 5.1 🧩 Comfort package
We created:
- `comfort_convenience_Package` with rule-based keywords:
  - Premium Plus / Premium / Standard

```python
premium = [...]
premium_plus = [...]

df["comfort_convenience_Package"] = df["comfort_convenience"].apply(
    lambda s: "Premium Plus" if all(w in s for w in premium_plus)
    else ("Premium" if all(w in s for w in premium) else "Standard")
)

df.drop("comfort_convenience", axis=1, inplace=True)
```

### 5.2 🎵 Entertainment package
Created:
- `entertainment_media_Package` (Media Plus vs Standard Media)

```python
media_plus = [...]
df["entertainment_media_Package"] = df["entertainment_media"].apply(
    lambda s: "Media Plus" if any(w in s for w in media_plus) else "Standard Media"
)
df.drop("entertainment_media", axis=1, inplace=True)
```

### 5.3 🛡️ Safety package
Created:
- `safety_security_Package` (Premium / Premium Plus / Standard)

```python
premium = [...]
premium_plus = [...]
df["safety_security_Package"] = df["safety_security"].apply(...)
df.drop("safety_security", axis=1, inplace=True)
```

✅ Why we engineered packages:
- Long equipment text is hard to model directly.
- Package level gives a strong, compact signal.

---

## 6) 🗑️ “Drop Strategy” in Part-02 (What we removed and why)
We dropped columns for clear reasons:

### 6.1 Helper columns (only for fixing other columns)
- `modified_make_model`, `short_description`, `extracted_models`

✅ Reason: they were only tools; keeping them adds noise.

### 6.2 Redundant columns (same signal already exists)
- `power_hp` (redundant with `power_kW`)
- `cons_city`, `cons_country` (redundant after choosing `cons_avg` as main)
- `cylinders` (considered low value / redundant with engine_size + power)

✅ Reason: keep the dataset focused and avoid multicollinearity/noise.

---

## 7) ✅ Quality Gates (How we verified our fills)
We repeatedly used:
- `first_looking(col)` before and after filling
- group-based summaries like `groupby(...).describe()` to detect patterns and sanity-check
- every fill function printed:
  - % null after fill
  - number of nulls
  - unique count
  - value counts

✅ This ensured:
- we didn’t “fill with nonsense”
- we didn’t break category distributions silently
- we could spot anomalies (example: Electric with non-zero emissions)

---

## 8) 💾 Final Deliverable
At the end:
- dataset had far fewer missing values
- grouping keys were stable
- engineered package columns existed
- helper/redundant columns were removed

```python
df.to_csv("filled_scout2022.csv", index=False)
```

---

# 🎯 Mini Decision Tree (Very Clear)
- **If `model` missing** → extract from `short_description` (regex) → if still missing → drop row  
- **If categorical** (doors/gearbox/fuel_type/drivetrain/seats) → `mode` with fallback groups  
- **If numeric & skewed** (co_emissions/cons_avg) → `median` with 3-level fallback  
- **If numeric & segment-average** (mileage) → `mean` by `(make_model, age)`  
- **If propagated attribute** (previous_owner/upholstery) → group `ffill+bfill`  
- **If domain-specific** (Electric) → handle Electric first (special rule), then general fill  
- **If long text equipment** → fill → create `*_Package` → drop raw text column  
- **If redundant** → drop
