# 🟥 Phase 3 Executive Summary  
## 🧼 Outlier Handling & Data Quality Stabilization (Scout 2022)

## 🟦 Executive Overview

The primary objective of **Phase 3** is to reduce noise originating from **data entry errors, extreme outliers, and duplicate records**—the main factors distorting price prediction performance—and to bring the dataset into a **model-ready, stable state**.

The approach taken in this phase is **not simple row deletion**. Instead, the strategy prioritizes **row preservation**, correcting faulty values through **NaN assignment followed by group-wise imputation** wherever feasible. As a result, the dataset now exhibits **more stable distributions** and **stronger domain-consistent logic**, improving downstream modeling reliability.

---

## 🟩 Scope & Deliverables

### ✅ In Scope

- 🎯 Outlier sanitation on the **price target variable**
- 🧠 Correction of *impossible / suspicious values* using domain rules
- 📦 Distribution-based outlier removal via **IQR (Tukey Fence)**
- 📈 Robust-like thresholding using **median-centered z-style filtering (z < 3)**
- ♻️ Duplicate record removal
- 🧾 Post-cleaning validation:
  - Distribution plots  
  - Null checks  
  - Correlation & multicollinearity scans  

---

## 📌 Outputs at Phase End

- ✅ Cleaned, **model-ready table**: **21,769 rows × 28 columns**
- ✅ Two columns intentionally dropped due to noise:
  - `doors`
  - `seats`
- ✅ Intermediate outputs suitable for **dummy encoding & feature engineering**  
  → Direct bridge to **Phase 4**

---

## 📊 Impact Summary

### 🧾 Net KPI Changes

- 🟦 Start: **28,624 rows × 30 columns**
- 🟩 End: **21,769 rows × 28 columns**
- 🔻 Net row reduction: **6,855 (~23.95%)**
- 🗑️ Column reduction: **2 (doors, seats)**

---

### 🧮 Top 4 Drivers of Row Loss (Business-Relevant)

| Driver | Rows Removed | Business Note |
|------|-------------|---------------|
| 💰 Price IQR cleaning | -1,914 | Largest early cut; stabilizes target |
| 📆 Age domain cut (>20 or <0) | -1,242 | High segment impact |
| ♻️ Duplicate removal | -1,470 | Pure quality improvement |
| ⚡ power_kW z-style outliers | -601 | May affect performance segment |

🎯 **Executive Insight:**  
Row loss is not driven by a single rule—**price, age, duplicates, and power_kW together define the character of Phase 3**.

---

## 🧠 Core Methodology: “3-Layer Data Quality Architecture”

Phase 3 treats outliers **progressively**, based on data quality context rather than a single blunt method.

---

### 1️⃣ 🧠 Domain Rules (Validity Rules)

**Goal:** Logical correctness *before* statistics.

Examples:
- `gears == 0` → invalid → **NaN**
- `mileage > 1,000,000` → extreme → **drop**
- `age < 0` → physically impossible → **drop**
- Unrealistic values in `empty_weight` → **NaN**

---

### 2️⃣ 📦 Distribution Rules (IQR / Tukey Fence)

**Goal:** Systematic trimming of distribution-breaking extremes.

- Applied primarily to **price** and **mileage**
- Makes the target distribution **learnable** and less loss-dominant

---

### 3️⃣ 📈 Robust-like Thresholding (Median-Centered z-style)

**Goal:** Catch tail outliers missed by hard rules.

Applied to:
- `engine_size`
- `co_emissions`
- `cons_avg`
- `power_kW`

🟦 **Note:**  
This approach is practical but not as robust as a true **MAD-based modified z-score**.  
→ Improvement proposed for Phase 4.

---

## 🧩 Key Decisions & Business Rationale

### 💰 1) `price` (Target Variable) — *Saving Model Learnability*

- ✅ Manual removal of obvious price anomalies
- ✅ Large-scale trimming via IQR

**Why?**  
Extreme target outliers dominate the loss function and distort global learning behavior.

**Trade-off:**  
Luxury / collector segments may be weakened → flagged as a business risk.

---

### 🔢 2) `gears` — *Statistical Outlier ≠ Domain Outlier*

- ⚡ Electric vehicles with `gears = 1` look like outliers statistically but are **domain-valid**
- 🚫 Values `0` and `>8` treated as invalid → **NaN**
- 🧩 Imputed using **mode by make_model + body_type** (609 values)
- 🧨 Single `gears == 2` record dropped (1 row)

**Rationale:**  
`gears` behaves like a **categorical feature**, not a continuous measurement.  
Mode imputation preserves rows and improves logical consistency.

---

### 🏋️ 3) `empty_weight` — *Fix the Value, Not the Row*

- 🚨 Physically impossible values detected (e.g. 15,590 kg)
- ✅ Rows preserved; values set to **NaN**
- 🧩 Group-wise mode imputation (3 values)

**Why?**  
Rows remain valuable across other features; single-cell corruption should not destroy full observations.

---

### 🌫️ 4) `co_emissions` — *Test Alternatives Before Dropping*

- ✅ Explored **winsorization** and **log transforms**
- 🚫 Extreme values treated as data quality issues → **NaN**
- 🧩 Median imputation
- 📈 Final z-style outlier drop (~200 rows)

**Why not only transform?**
- Winsorize/log help *distribution shape*
- But some values were fundamentally implausible → correction + drop was justified

---

## 🔍 Quality Control Outputs

### ✅ Distribution Stabilization

- Post-cleaning histograms and boxplots became interpretable
- Key features stabilized:
  - `empty_weight`
  - `co_emissions`
  - `cons_avg`
  - `power_kW`
- Target `price` no longer dominated by extreme tails

---

### ✅ Multicollinearity Scan (|corr| ≥ 0.6)

| Feature Pair |
|--------------|
| age ↔ mileage |
| co_emissions ↔ cons_avg |
| engine_size ↔ power_kW |
| empty_weight ↔ power_kW |

**Business Meaning:**  
These pairs likely encode overlapping information → feature selection or regularization required in Phase 4.

---

## ⚠️ Risks & Executive-Level Warnings

### 🔶 Segment Exclusion Risk
- Dropping `age > 20` removes **classic / youngtimer** vehicles
- Acceptable for mainstream used-car market, risky otherwise

### 🔶 Performance Segment Risk
- Rare high `power_kW` trims may be disproportionately affected

### 🔶 Rule-Based Standardization Risk
- Assumptions like “Mustang = 6 gears” improve consistency
- But may ignore year/trim-level variance

---

## 🧭 Clear Phase 4 Recommendations

- 🛡️ Adopt **MAD-based modified z-score** for robust outlier detection
- 🧩 Use **group-wise thresholds** (make/model) instead of global IQR for price & mileage
- 🧱 Move all cleaning, imputation, encoding into a **Pipeline / ColumnTransformer**  
  → *fit on train only*
- 🧾 Maintain a **rule registry** with rationale, impact, and row counts (governance)
- 📈 Perform **bias & segment impact analysis** for age and performance-related cuts

---

## 🟦 One-Sentence Executive Conclusion

**Phase 3 successfully reduced high-noise outliers and duplicates, delivering a more stable, consistent, and model-ready dataset; however, age cutoffs and performance-segment decisions require explicit bias and segment analysis in Phase 4.**
