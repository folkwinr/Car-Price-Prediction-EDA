## A) Pipeline Columns (Phase 1 → Phase 3)

| Column | Phase 1 (Data Cleaning) | Phase 2 (Missing Values) | Phase 3 (Outliers + Final Step) | Final Status |
|---|---|---|---|---|
| make_model | ✅ snake_case + basic text standardization (used as brand+model identity). | 🔧 After fixing `model`, rebuilt using **make + model**; `.str.title()` for consistent format. | 🧭 Used as a grouping key (not an outlier target). | ✅ Kept in Final |
| short_description | ✅ Kept (helper text for model/identity checks). | 🧠 Used to recover `model` via regex; then **dropped** after finishing. | — | ❌ Removed in Phase 2 |
| make | ✅ Text cleanup/standardization (brand). | 🔤 `.str.title()` formatting (used for make_model rebuild). | — | ✅ Kept in Final |
| model | ✅ Text cleanup/standardization. | 🧠 Extracted from `short_description` with regex + `fillna`; a few unrecoverable rows were **dropped**. | — | ✅ Kept in Final |
| location | ✅ Cleaned/standardized (string). | — | — | ✅ Kept in Final |
| price | 🔢 Numeric conversion + format cleanup (€, separators, etc.). | — | 🚨 Domain filter + **IQR (Tukey Fence)** to drop extreme rows. | ✅ Kept in Final |
| body_type | ✅ Category cleanup/standardization. | 🔤 `.str.title()` for consistent grouping. | 🧭 Used as grouping key (not an outlier target). | ✅ Kept in Final |
| type | ✅ Category cleanup/standardization. | — | — | ✅ Kept in Final |
| doors | 🔢 Numeric/format check (category/numeric cleanup). | 🧩 Group-based **mode fill** (make_model + body_type → fallback). | 🗑 Entire column **dropped** (low contribution / unstable). | ❌ Removed in Phase 3 |
| warranty | ✅ Basic cleanup (string). | 🧾 Rule-based: `-` → **No**, otherwise → **Yes** (binary). | — | ✅ Kept in Final |
| mileage | 🔢 Numeric conversion + format cleanup. | 📈 **Mean fill** inside `make_model + age` segments. | 🚨 `> 1,000,000` drop + **IQR (Tukey)** to drop remaining extremes. | ✅ Kept in Final |
| gearbox | ✅ Category cleanup/standardization. | 🧩 Group-based **mode fill**. | — | ✅ Kept in Final |
| fuel_type | ✅ Category cleanup/standardization. | 🧩 Group-based **mode fill** (make_model + gearbox) + 1 manual fix (single record). | — | ✅ Kept in Final |
| seller | ✅ Category cleanup/standardization. | — | — | ✅ Kept in Final |
| seats | 🔢 Numeric/format check. | 🧩 Group-based **mode fill**. | 🗑 Entire column **dropped**. | ❌ Removed in Phase 3 |
| engine_size | 🔢 Numeric conversion + format cleanup. | 🧩 `-` → NaN; group-based **mode fill** (make_model + body_type). | 🚨 Known invalid set → NaN; then **mode fill**; remaining extremes removed via z-score. | ✅ Kept in Final |
| gears | 🔢 Numeric/format cleanup. | 🧩 `-` → NaN; multi-level group-based **mode fill** (make_model/body_type/gearbox → fallback). | 🚨 `0` or `>8` → NaN + mode fill; `==2` rows dropped. | ✅ Kept in Final |
| co_emissions | 🔢 Numeric conversion + format cleanup. | ⚡ Electric-specific checks + segment **median fill** (multi-level fallback). | 🚨 Extreme values → NaN; **median fill**; log1p review; z-score row drops. | ✅ Kept in Final |
| drivetrain | ✅ Category cleanup/standardization. | 🧩 Group-based **mode fill**. | — | ✅ Kept in Final |
| cylinders | 🔢 Numeric/format cleanup. | 🧩 Mode filled; later considered low value/redundant → **dropped**. | — | ❌ Removed in Phase 2 |
| empty_weight | 🔢 Numeric conversion + format cleanup. | 🧩 Group-based **mode fill**. | 🚨 `>4000` and {75, 525} → NaN; then mode fill. | ✅ Kept in Final |
| full_service_history | ✅ Category cleanup/standardization. | — | — | ✅ Kept in Final |
| upholstery | ✅ Category cleanup/standardization. | 🪑 Category consolidation (Velour→Cloth etc.); `Other`→NaN; group ffill/bfill. | — | ✅ Kept in Final |
| previous_owner | 🔢 Numeric/format cleanup. | 🔁 ffill/bfill propagation within `age` groups. | 🚨 Rows with `>=10` dropped. | ✅ Kept in Final |
| energy_efficiency_class | ✅ Category cleanup (string). | 🧩 Group-based **mode fill** (`make_model + age` → fallback). | — | ✅ Kept in Final |
| extras | 🧾 List/text cleaned (stringified). | 🧩 Group-based **mode fill**. | — | ✅ Kept in Final |
| age | 🧠 **Feature Engineering:** `age = 2022 - first_registration` | 🧓 Domain rule: if `mileage < 10000` and age missing → set `0` (new car). | 🚨 Drop rows where `age < 0` or `age > 20`. | ✅ Kept in Final |
| power_kW | 🧠 **Feature Engineering:** extracted `power_kW` and `power_hp` from power text (regex); numeric. | 🧩 `-`→NaN; group-based **mode fill** (`make_model + body_type`). | 🚨 Low-frequency kW values → NaN; segment **median fill**; z-score row drops. | ✅ Kept in Final |
| power_hp | 🧠 Extracted from power field (numeric). | 🧩 Group-based **mode fill**; then redundant with `power_kW` → **dropped**. | — | ❌ Removed in Phase 2 |
| cons_avg | 🧠 **Feature Engineering:** extracted from `fuel_consumption`; numeric. | ⚡ Electric set to constant; remaining filled with segment **median**. | 🚨 `>=20` → NaN; median fill; z-score row drops. | ✅ Kept in Final |
| cons_city | 🧠 Extracted from `fuel_consumption`. | 🗑 Redundant after selecting `cons_avg` → **dropped**. | — | ❌ Removed in Phase 2 |
| cons_country | 🧠 Extracted from `fuel_consumption`. | 🗑 Redundant after selecting `cons_avg` → **dropped**. | — | ❌ Removed in Phase 2 |
| comfort_convenience | 🧾 List/text cleanup (stringified). | 🧩 Mode fill → **Package feature** created → raw column **dropped**. | — | ❌ Removed in Phase 2 |
| entertainment_media | 🧾 List/text cleanup (stringified). | 🧩 Mode fill → **Package feature** created → raw column **dropped**. | — | ❌ Removed in Phase 2 |
| safety_security | 🧾 List/text cleanup (stringified). | 🧩 Mode fill → **Package feature** created → raw column **dropped**. | — | ❌ Removed in Phase 2 |
| comfort_convenience_Package | — | 🧪 Feature Engineering: comfort text → **Standard / Premium / Premium Plus** package level. | — | ✅ Kept in Final |
| entertainment_media_Package | — | 🧪 Feature Engineering: media text → **Standard Media / Media Plus**. | — | ✅ Kept in Final |
| safety_security_Package | — | 🧪 Feature Engineering: safety text → **Standard / Premium / Premium Plus**. | — | ✅ Kept in Final |

---

## B) Temporary Helper Columns

| Column | Phase 1 (Data Cleaning) | Phase 2 (Missing Values) | Phase 3 (Outliers + Final Step) | Final Status |
|---|---|---|---|---|
| extracted_models (helper) | — | 🧠 Temporary column from regex extraction; dropped after filling `model`. | — | ❌ Removed in Phase 2 |
| modified_make_model (helper) | — | 🔧 Temporary identity from make+model; dropped after updating `make_model`. | — | ❌ Removed in Phase 2 |

---

## C) Columns Removed in Phase 1 (Raw-only / High Missing / Out of Scope)

| Column | Phase 1 (Data Cleaning) | Phase 2 (Missing Values) | Phase 3 (Outliers + Final Step) | Final Status |
|---|---|---|---|---|
| availability | 🗑 Very high missing / low use (>%80 NaN) → bulk **drop**. | — | — | ❌ Removed in Phase 1 |
| available_from | 🗑 Very high missing / low use (>%80 NaN) → bulk **drop**. | — | — | ❌ Removed in Phase 1 |
| battery_ownership | 🗑 Very high missing / low use (>%80 NaN) → bulk **drop**. | — | — | ❌ Removed in Phase 1 |
| co_efficiency | 🗑 Very high missing / low use (>%80 NaN) → bulk **drop**. | — | — | ❌ Removed in Phase 1 |
| co_emissions_wltp | 🗑 Very high missing / low use (>%80 NaN) → bulk **drop**. | — | — | ❌ Removed in Phase 1 |
| colour | 🗑 Low value / redundant / out of scope → **drop**. | — | — | ❌ Removed in Phase 1 |
| country_version | 🗑 Low value / redundant / out of scope → **drop**. | — | — | ❌ Removed in Phase 1 |
| desc | 🗑 Low value / redundant / out of scope → **drop**. | — | — | ❌ Removed in Phase 1 |
| electric_range_wltp | 🗑 Very high missing / low use (>%80 NaN) → bulk **drop**. | — | — | ❌ Removed in Phase 1 |
| emission_class | 🗑 Low value / redundant / out of scope → **drop**. | — | — | ❌ Removed in Phase 1 |
| emissions_sticker | 🗑 Low value / redundant / out of scope → **drop**. | — | — | ❌ Removed in Phase 1 |
| first_registration | 🧠 Source column: used to create a new feature, then **dropped**. | — | — | ❌ Removed in Phase 1 |
| fuel_consumption | 🧠 Source column: used to create new features, then **dropped**. | — | — | ❌ Removed in Phase 1 |
| fuel_consumption_wltp | 🗑 Very high missing / low use (>%80 NaN) → bulk **drop**. | — | — | ❌ Removed in Phase 1 |
| general_inspection | 🗑 Low value / redundant / out of scope → **drop**. | — | — | ❌ Removed in Phase 1 |
| last_service | 🗑 Very high missing / low use (>%80 NaN) → bulk **drop**. | — | — | ❌ Removed in Phase 1 |
| last_timing_belt_change | 🗑 Very high missing / low use (>%80 NaN) → bulk **drop**. | — | — | ❌ Removed in Phase 1 |
| manufacturer_colour | 🗑 Low value / redundant / out of scope → **drop**. | — | — | ❌ Removed in Phase 1 |
| model_code | 🗑 Low value / redundant / out of scope → **drop**. | — | — | ❌ Removed in Phase 1 |
| non_smoker_vehicle | 🗑 Low value / redundant / out of scope → **drop**. | — | — | ❌ Removed in Phase 1 |
| offer_number | 🗑 Low value / redundant / out of scope → **drop**. | — | — | ❌ Removed in Phase 1 |
| other_fuel_types | 🗑 Very high missing / low use (>%80 NaN) → bulk **drop**. | — | — | ❌ Removed in Phase 1 |
| paint | 🗑 Low value / redundant / out of scope → **drop**. | — | — | ❌ Removed in Phase 1 |
| power | 🧠 Source column: used to create new features, then **dropped**. | — | — | ❌ Removed in Phase 1 |
| power_consumption | 🗑 Very high missing / low use (>%80 NaN) → bulk **drop**. | — | — | ❌ Removed in Phase 1 |
| power_consumption_wltp | 🗑 Very high missing / low use (>%80 NaN) → bulk **drop**. | — | — | ❌ Removed in Phase 1 |
| production_date | 🧠 Source column: used to create a new feature, then **dropped**. | — | — | ❌ Removed in Phase 1 |
| taxi_or_rental_car | 🗑 Very high missing / low use (>%80 NaN) → bulk **drop**. | — | — | ❌ Removed in Phase 1 |
| upholstery_colour | 🗑 Low value / redundant / out of scope → **drop**. | — | — | ❌ Removed in Phase 1 |
