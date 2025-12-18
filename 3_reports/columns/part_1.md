# ✅ Part-01 (Data Cleaning) — Column-by-Column Operations (Raw → Clean)
This document explains, **for every raw column**, what we did in Part-01:
- rename to snake_case
- cleaning / parsing steps (explode, regex, mapping, fill)
- final status: **kept / dropped / used to create new features**

**Global steps applied first**
- ✅ `df = df0.copy()` to protect raw data
- ✅ `dropna(how="all")` to remove fully empty rows
- ✅ column names standardized with `to_snake_case()`
- ✅ high-missing columns removed with a rule like **>80% missing → drop** (some columns below are dropped by this rule)
- ✅ duplicates were checked (workaround used when list-types exist)

---

## A) Listing Identity & Seller

### `make_model` → `make_model`
- **Operations:** basic inspection (`first_looking`), no parsing needed
- **Final:** ✅ **KEPT** (core segmentation feature)

### `short_description` → `short_description`
- **Operations:** inspected; no special transformation
- **Final:** ✅ **KEPT**

### `make` → `make`
- **Operations:** trimmed newline characters  
  - example: `df["make"] = df["make"].str.strip("\n")`
- **Final:** ✅ **KEPT**

### `model` → `model`
- **Operations:** list-to-text handling using `explode()` + `strip()`  
  - example: `df["model"] = df["model"].explode().str.strip("\n, ")`
- **Final:** ✅ **KEPT**
- **Note (risk):** `explode()` can increase row count if lists have >1 item.

### `location` → `location`
- **Operations:** inspected; no special transformation
- **Final:** ✅ **KEPT**

### `Offer number` → `offer_number`
- **Operations:** dropped (ID-like / leakage risk)
- **Final:** ❌ **DROPPED**

### `seller` → `seller`
- **Operations:** inspected; no special transformation
- **Final:** ✅ **KEPT**

### `Country version` → `country_version`
- **Operations:** inspected; considered low value / very missing
- **Final:** ❌ **DROPPED**

### `Model code` → `model_code`
- **Operations:** inspected; considered low value / very missing
- **Final:** ❌ **DROPPED**

### `desc` → `desc`
- **Operations:** free text; dropped (NLP not in scope for Part-01)
- **Final:** ❌ **DROPPED**

---

## B) Price & Usage

### `price` → `price`
- **Operations:** text → numeric using regex + separator cleanup  
  - extract number, remove `,`, convert to float
- **Final:** ✅ **KEPT** (most important column)

### `Mileage` → `mileage`
- **Operations:** separator cleanup + regex extract → numeric  
  - example: remove commas, extract digits, convert to float
- **Final:** ✅ **KEPT**

---

## C) Body & Interior / Exterior

### `Body type` → `body_type`
- **Operations:** `explode()` + `strip()` cleanup
- **Final:** ✅ **KEPT**
- **Note (risk):** same `explode()` risk (row expansion) if lists contain >1 item.

### `Type` → `type`
- **Operations:** `explode()` + `strip()` cleanup
- **Final:** ✅ **KEPT**

### `Doors` → `doors`
- **Operations:** `explode()` + `strip()` then numeric conversion  
  - example: `pd.to_numeric(df["doors"])`
- **Final:** ✅ **KEPT**

### `Seats` → `seats`
- **Operations:** list-safe conversion + regex extract digits → numeric  
  - first element if list, then `extract` digits, convert to float
- **Final:** ✅ **KEPT**

### `Colour` → `colour`
- **Operations:** inspected; compared with manufacturer color
- **Final:** ❌ **DROPPED** (high missing / low value for this phase)

### `Manufacturer colour` → `manufacturer_colour`
- **Operations:** inspected together with `colour`
- **Final:** ❌ **DROPPED**

### `Paint` → `paint`
- **Operations:** filled missing with a default value (example: `"Uni/basic"`)
- **Final:** ❌ **DROPPED** (later removed)

### `Upholstery colour` → `upholstery_colour`
- **Operations:** mapped into broader color groups (via `coloridentifier()`)
- **Final:** ❌ **DROPPED** (later removed)

### `Upholstery` → `upholstery`
- **Operations:** inspected; no heavy parsing
- **Final:** ✅ **KEPT**

---

## D) Engine / Powertrain / Technical

### `Power` → `power` (then split)
- **Operations:**
  - list-safe conversion (take first element if list)
  - regex split into two numeric fields:
    - `power_kW`
    - `power_hp`
- **Final:**  
  - `power`: ❌ **DROPPED**  
  - `power_kW`: ✅ **KEPT**  
  - `power_hp`: ✅ **KEPT**

### `Engine size` → `engine_size`
- **Operations:** remove separators + regex extract digits → numeric
- **Final:** ✅ **KEPT**

### `Cylinders` → `cylinders`
- **Operations:** `astype(str)` + regex extract digits → numeric
- **Final:** ✅ **KEPT**

### `Gearbox` → `gearbox`
- **Operations:** string cleanup + extract non-digit part  
  - also replaced incorrect leftover values (example: `'a'`) with NaN
- **Final:** ✅ **KEPT**

### `Gears` → `gears`
- **Operations:** regex extract digits → numeric
- **Final:** ✅ **KEPT**

### `Drivetrain` → `drivetrain`
- **Operations:** `explode()` + `strip()` cleanup
- **Final:** ✅ **KEPT**

### `Empty weight` → `empty_weight`
- **Operations:** remove separators + regex extract digits → numeric
- **Final:** ✅ **KEPT**

---

## E) Fuel & Consumption

### `Fuel type` → `fuel_type`
- **Operations:**
  - split on `/` and take first part
  - mapping function `fueltype()` to group similar fuel labels
- **Final:** ✅ **KEPT**

### `Other fuel types` → `other_fuel_types`
- **Operations:** dropped mainly due to very high missing values (rule-based)
- **Final:** ❌ **DROPPED**

### `Fuel consumption` → `fuel_consumption` (then split)
- **Operations:**
  - helper functions select parts (avg/city/country) from list/nested data
  - regex extract numeric value → float
  - created:
    - `cons_avg`
    - `cons_city`
    - `cons_country`
- **Final:**  
  - `fuel_consumption`: ❌ **DROPPED**  
  - `cons_avg`: ✅ **KEPT**  
  - `cons_city`: ✅ **KEPT**  
  - `cons_country`: ✅ **KEPT**

### `Fuel consumption (WLTP)` → `fuel_consumption_wltp`
- **Operations:** dropped due to very high missing values (rule-based)
- **Final:** ❌ **DROPPED**

---

## F) EV / Electric Fields

### `Power consumption` → `power_consumption`
- **Operations:** dropped due to very high missing values (rule-based)
- **Final:** ❌ **DROPPED**

### `Power consumption (WLTP)` → `power_consumption_wltp`
- **Operations:** dropped due to very high missing values (rule-based)
- **Final:** ❌ **DROPPED**

### `Electric Range (WLTP)` → `electric_range_wltp`
- **Operations:** dropped due to very high missing values (rule-based)
- **Final:** ❌ **DROPPED**

### `Battery Ownership` → `battery_ownership`
- **Operations:** dropped due to very high missing values (rule-based)
- **Final:** ❌ **DROPPED**

---

## G) Emissions & Efficiency

### `CO₂-emissions` → `co_emissions`
- **Operations:** `astype(str)` + regex extract digits → numeric
- **Final:** ✅ **KEPT**

### `CO₂-emissions (WLTP)` → `co_emissions_wltp`
- **Operations:** dropped due to very high missing values (rule-based)
- **Final:** ❌ **DROPPED**

### `CO₂-efficiency` → `co_efficiency`
- **Operations:** inspected; considered low value for this phase
- **Final:** ❌ **DROPPED**

### `Emission class` → `emission_class`
- **Operations:** normalized using `emissionclass()` (grouped Euro variants)
- **Final:** ❌ **DROPPED** (later removed)

### `Emissions sticker` → `emissions_sticker`
- **Operations:** inspected with value counts
- **Final:** ❌ **DROPPED**

### `Energy efficiency class` → `energy_efficiency_class`
- **Operations:** grouped into broader labels using `energyefficiency()`
  - example groups: `"efficient"` vs `"unefficient"`
- **Final:** ✅ **KEPT**

---

## H) Service / History / Inspection

### `First registration` → `first_registration` (then used for age)
- **Operations:**
  - extracted year (last 4 characters)
  - created `age = reference_year - first_registration_year`
- **Final:**  
  - `first_registration`: ❌ **DROPPED**  
  - `age`: ✅ **KEPT**

### `Production date` → `production_date`
- **Operations:** removed after `age` was created (not needed anymore)
- **Final:** ❌ **DROPPED**

### `Previous owner` → `previous_owner`
- **Operations:** extracted a character position (string indexing)
- **Final:** ✅ **KEPT**
- **Note (risk):** string indexing is fragile; regex digit extraction would be safer.

### `Warranty` → `warranty`
- **Operations:** list-safe conversion + regex digit extraction → numeric
- **Final:** ✅ **KEPT**

### `Full service history` → `full_service_history`
- **Operations:** filled missing values with `"No"`
- **Final:** ✅ **KEPT**

### `General inspection` → `general_inspection`
- **Operations:** considered low value for this phase
- **Final:** ❌ **DROPPED**

### `Non-smoker vehicle` → `non_smoker_vehicle`
- **Operations:** filled missing with `"No"`, then removed
- **Final:** ❌ **DROPPED**

### `Last service` → `last_service`
- **Operations:** dropped due to very high missing values (rule-based)
- **Final:** ❌ **DROPPED**

### `Last timing belt change` → `last_timing_belt_change`
- **Operations:** dropped due to very high missing values (rule-based)
- **Final:** ❌ **DROPPED**

### `Taxi or rental car` → `taxi_or_rental_car`
- **Operations:** dropped due to very high missing values (rule-based)
- **Final:** ❌ **DROPPED**

---

## I) Availability

### `Availability` → `availability`
- **Operations:** dropped due to very high missing values (rule-based)
- **Final:** ❌ **DROPPED**

### `Available from` → `available_from`
- **Operations:** dropped due to very high missing values (rule-based)
- **Final:** ❌ **DROPPED**

---

## J) Equipment Groups (4 columns with newline characters in raw names)

### `\nComfort & Convenience\n` → `comfort_convenience`
- **Operations:**
  - copied into a clean column name
  - converted list → readable text (join with `", "`)
  - dropped the raw newline-named column
- **Final:** ✅ **KEPT** (as text)

### `\nEntertainment & Media\n` → `entertainment_media`
- **Operations:** list → joined text
- **Final:** ✅ **KEPT** (as text)

### `\nSafety & Security\n` → `safety_security`
- **Operations:** list → joined text
- **Final:** ✅ **KEPT** (as text)

### `\nExtras\n` → `extras`
- **Operations:** list → joined text
- **Final:** ✅ **KEPT** (as text)

---

## New Features Created in Part-01 (Not in raw columns)
- ✅ `age` (from `first_registration`)
- ✅ `power_kW` and `power_hp` (from `power`)
- ✅ `cons_avg`, `cons_city`, `cons_country` (from `fuel_consumption`)
