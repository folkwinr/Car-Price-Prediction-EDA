# ✅ Part-02 (Handling Missing Values) — Column-by-Column Operations (Clean → Filled)
This document explains, **for every column in Part-02**, what we did **step by step**:
- what we checked
- what we decided
- which method we applied (mode/median/mean/ffill, regex extraction, manual fix)
- the final status (**kept / dropped / replaced by new feature**)

📌 **Part-02 starting point**
- Input: `clean_scout2022.csv`
- Start shape: **28,630 rows — 35 columns**
- End shape: **28,624 rows — 30 columns** ✅  
  (we dropped **6 rows** where `model` could not be recovered + we dropped some redundant columns)

---

## 1) Identity / Core Description Columns

### ✅ `make_model`
**What we checked**
- This column is a main **group key** in Part-02; it must be clean for group-based filling.

**What we did (step by step)**
1) After fixing `model`, we created a more reliable combined label:
   - `modified_make_model = make + " " + model`
2) If `modified_make_model` had missing values, we completed it using the old `make_model`.
3) We replaced `make_model` with `modified_make_model`.
4) We also fixed some naming inconsistencies using `replace(...)` (example: unusual brand/model text cases).
5) We standardized text using `.str.title()` for consistent formatting.

**Final**
- ✅ **KEPT**, and improved for stable grouping.

---

### ❌ `short_description` (dropped at the end)
**What we checked**
- Missing rate was small, but it was useful as a text source.

**What we did**
- We used it as a **helper column** to extract missing `model` values using a large regex pattern.
- We did not “fill” `short_description`; we used it to **repair model**.

**Why dropped**
- After `model` was completed, this column was not needed for the filled dataset.

**Final**
- ❌ **DROPPED**

---

### ✅ `make`
**What we did**
- Used to rebuild `make_model` (`make + model`)
- Standardized with `.str.title()`

**Final**
- ✅ **KEPT**

---

### ✅ `model` (most important Part-02 fix)
**What we checked**
- Missing rate was small, but the impact was big because `model` affects grouping.

**What we did (step by step)**
1) Built a strong `model_pattern` (regex).
2) Extracted candidate models from `short_description`:
   - `extracted_models = short_description.str.extract(...).bfill(axis=1)[0]`
3) Filled missing `model` using `extracted_models`:
   - `model.fillna(extracted_models, inplace=True)`
4) Listed remaining missing model rows and inspected them.
5) Dropped rows where `model` could not be recovered:
   - `df.dropna(subset=["model"], inplace=True)`

**Final**
- ✅ **KEPT**, now complete (this is why rows dropped from 28,630 to 28,624)

---

### ✅ `location`
- No missing / no transformation in Part-02
- ✅ **KEPT**

---

### ✅ `price`
- No missing / not filled
- Used as a reference column for sanity checks (distribution checks for other fills)
- ✅ **KEPT**

---

## 2) Body / Type Columns

### ✅ `body_type`
**What we did**
- Standardized formatting:
  - `.str.title()`
**Why**
- Cleaner grouping (same class should look the same)

**Final**
- ✅ **KEPT**

---

### ✅ `type`
- No Part-02 transformation (mostly a stable descriptive column)
- ✅ **KEPT**

---

### ✅ `doors`
**What we checked**
- Missing exists and is strongly related to `make_model` and `body_type`.

**What we did**
- Filled using **hierarchical mode logic**:
  1) mode within `(make_model + body_type)`
  2) fallback: mode within `make_model`
  3) fallback: global mode

**Final**
- ✅ **KEPT**, missing removed.

---

## 3) Engine / Gear / Technical Columns

### ✅ `engine_size`
**What we checked**
- Missing existed and some values were fake-missing like `"-"`.

**What we did**
1) Convert `"-"` to `NaN`
2) Group-based fill using mode:
   - `fill(df, "make_model", "body_type", "engine_size", "mode")`
   - fallback: `(make_model+body_type)` → `make_model` → global

**Final**
- ✅ **KEPT**

---

### ✅ `gearbox`
**What we did**
1) Temporarily used `"-"` for visibility, then converted back to `NaN`
2) Filled using:
   - `fill(df, "make_model", "body_type", "gearbox", "mode")`

**Final**
- ✅ **KEPT**

---

### ✅ `gears`
**What we checked**
- Very high missing rate.
- Strong relationship with `gearbox`, `make_model`, `body_type`.

**What we did**
1) `"-"` visibility → `NaN`
2) Multi-level hierarchical **mode** fill:
   - `(make_model + body_type + gearbox)` → `(make_model + body_type)` → `(make_model)` → global

**Final**
- ✅ **KEPT**, large missing reduction.

---

### ✅ `drivetrain`
**What we checked**
- High missing rate, but strong link to model/body.

**What we did**
- `fill(df, "make_model", "body_type", "drivetrain", "mode")`

**Final**
- ✅ **KEPT**

---

### ✅ `empty_weight`
**What we checked**
- High missing rate; weight is usually stable within model/body segments.

**What we did**
- `fill(df, "make_model", "body_type", "empty_weight", "mode")`

**Final**
- ✅ **KEPT**

---

### ❌ `cylinders` (filled, then dropped)
**What we did**
- First filled with mode:
  - `fill(df, "make_model", "body_type", "cylinders", "mode")`
- Then dropped:
  - `df.drop("cylinders", axis=1, inplace=True)`

**Why dropped**
- Considered low value / redundant (engine_size + power already represent engine well)

**Final**
- ❌ **DROPPED**

---

## 4) Performance Columns

### ✅ `power_kW`
**What we did**
- Filled using mode in `(make_model + body_type)`:
  - `fill(df, "make_model", "body_type", "power_kW", "mode")`

**Final**
- ✅ **KEPT**

---

### ❌ `power_hp` (filled, then dropped)
**What we did**
- Filled first (same approach as kW):
  - `fill(df, "make_model", "body_type", "power_hp", "mode")`
- Dropped later:
  - `df.drop("power_hp", axis=1, inplace=True)`

**Why dropped**
- Fully redundant with `power_kW` (same signal, different unit)

**Final**
- ❌ **DROPPED**

---

## 5) Age / Mileage / Ownership

### ✅ `age`
**What we checked**
- Very low missing, but important for grouping and logic rules.

**What we did**
1) Used `"-"` temporarily to see missing clearly
2) Domain rule:
   - if `mileage < 10000` and `age` is missing → set `age = 0` (new car assumption)
3) Used group stats (by age) to sanity-check mileage patterns

**Final**
- ✅ **KEPT**

---

### ✅ `mileage`
**What we did**
- Filled missing (if any) using grouped mean:
  - `mileage.fillna(groupby(["make_model","age"]).mean())`
- Also compared overall mean vs segment mean for sanity checks

**Final**
- ✅ **KEPT**

---

### ✅ `previous_owner`
**What we checked**
- Very high missing rate.

**What we did**
1) `"-"` visibility → `NaN`
2) Filled by propagation within `age` groups:
   - `fill_prop(df, "age", "previous_owner")` (ffill + bfill)

**Final**
- ✅ **KEPT**

---

## 6) Fuel / Emissions / Consumption

### ✅ `fuel_type`
**What we checked**
- Missing exists; fuel type is linked to model and gearbox.

**What we did**
1) Filled using mode:
   - `fill(df, "make_model", "gearbox", "fuel_type", "mode")`
2) Manual correction for one record:
   - `df.loc[5831, "fuel_type"] = "Benzine"`

**Final**
- ✅ **KEPT**

---

### ✅ `co_emissions`
**What we checked**
- High missing rate.
- Electric cars are special (often 0 or very low).

**What we did (layered)**
1) Electric subgroup check:
   - inspected `co_emissions` distribution for `fuel_type == "Electric"`
   - filled Electric missing using Electric mode
   - checked anomalies (Electric but emissions not near expected)
2) Global fill using multi-level **median**:
   - `fill_median(df, "make_model", "body_type", "fuel_type", "co_emissions")`
   - fallback: (3-level) segment → broader segment → global median

**Final**
- ✅ **KEPT**

---

### ✅ `cons_avg`
**What we checked**
- Missing exists; Electric consumption behaves differently.

**What we did**
1) Domain rule for Electric:
   - set `cons_avg = 2.359` for Electric cars
2) Built a validation idea:
   - `cons_avg2 = (cons_country + cons_city) / 2` (check logic when both exist)
3) Filled remaining missing using multi-level **median**:
   - `fill_median(..., "cons_avg")`

**Final**
- ✅ **KEPT** (main consumption feature)

---

### ❌ `cons_city` (dropped)
**What we did**
- Dropped after choosing `cons_avg` as the main consumption feature:
  - `df.drop("cons_city", axis=1, inplace=True)`

**Final**
- ❌ **DROPPED**

---

### ❌ `cons_country` (dropped)
**What we did**
- Dropped for the same reason as `cons_city`:
  - `df.drop("cons_country", axis=1, inplace=True)`

**Final**
- ❌ **DROPPED**

---

## 7) Interior / Equipment Columns

### ✅ `upholstery`
**What we checked**
- High missing and many messy categories.

**What we did**
1) Category consolidation (domain-based):
   - `"Velour" → "Cloth"`
   - `"alcantara" / "Part leather" / "Full leather" → "Part/Full Leather"`
   - `"Other" → NaN` (treated as noise)
2) Missing handling:
   - `"-"` visibility → `NaN`
   - `fill(df, "make_model", "body_type", "upholstery", "ffill")`
   - (group ffill+bfill with fallbacks)

**Final**
- ✅ **KEPT**

---

### ❌ `comfort_convenience` (replaced by package feature)
**What we did**
1) Filled missing:
   - `fill(df, "make_model", "body_type", "comfort_convenience", "mode")`
2) Feature engineering:
   - created `comfort_convenience_Package` using keyword rules
3) Dropped the raw column:
   - `df.drop("comfort_convenience", axis=1, inplace=True)`

**Final**
- ❌ raw column **DROPPED**  
- ✅ `comfort_convenience_Package` **KEPT**

---

### ❌ `entertainment_media` (replaced by package feature)
**What we did**
1) Filled missing:
   - `fill(df, "make_model", "body_type", "entertainment_media", "mode")`
2) Feature engineering:
   - created `entertainment_media_Package` using keyword rules
3) Dropped the raw column

**Final**
- ❌ raw column **DROPPED**  
- ✅ `entertainment_media_Package` **KEPT**

---

### ❌ `safety_security` (replaced by package feature)
**What we did**
1) Filled missing:
   - `fill(df, "make_model", "body_type", "safety_security", "mode")`
2) Feature engineering:
   - created `safety_security_Package` using keyword rules
3) Dropped the raw column

**Final**
- ❌ raw column **DROPPED**  
- ✅ `safety_security_Package` **KEPT**

---

### ✅ `extras`
**What we checked**
- Missing exists, list/text column.

**What we did**
- Filled with mode within `(make_model + body_type)`:
  - `fill(df, "make_model", "body_type", "extras", "mode")`

**Final**
- ✅ **KEPT**

---

## 8) Columns kept with no major Part-02 changes
### ✅ `seller`
- No missing / no changes
- ✅ **KEPT**

### ✅ `full_service_history`
- No missing / no changes
- ✅ **KEPT**

### ✅ `energy_efficiency_class`
- Filled/handled using group mode (make_model + age in the notebook logic)
- ✅ **KEPT**

### ✅ `seats`
- Filled using mode within (make_model + body_type)
- ✅ **KEPT**

### ✅ `warranty`
- Converted into a Yes/No style meaning (rule-based classifier)
- ✅ **KEPT**

---

## 9) Helper columns created and removed in Part-02
### ❌ `extracted_models`
- Created from regex extraction on `short_description`
- Used only to fill `model`
- Dropped at the end

### ❌ `modified_make_model`
- Created from `make + model`
- Used to rebuild `make_model`
- Dropped at the end

---

## ✅ Final column set after Part-02 (30 columns)
`make_model, make, model, location, price, body_type, type, doors, warranty, mileage, gearbox, fuel_type, seller, seats, engine_size, gears, co_emissions, drivetrain, empty_weight, full_service_history, upholstery, previous_owner, energy_efficiency_class, extras, age, power_kW, cons_avg, comfort_convenience_Package, entertainment_media_Package, safety_security_Package`
