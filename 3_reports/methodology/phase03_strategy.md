# 🧭 Phase 03 Methodology  
## Outlier Handling Strategy & Decision Logic

Outlier handling in Phase 03 was **not treated as a single “magic formula”**.  
Instead, decisions were made based on **column type** and **error nature**.

- 🎯 If the **target (price)** is polluted, *all downstream analysis becomes misleading* → price handled first.
- 🧠 When values were **clearly wrong or impossible**, we preferred **NaN + group-wise imputation** over aggressive row drops.
- 🧱 For **heavy-tailed distributions**, **IQR (Tukey Fence)** was favored over z-score.
- 🎛️ For **discrete features** (e.g. `gears`, `previous_owner`), outlier logic was **domain-driven**, not statistical.
- ✅ After *every intervention*, we re-checked:
  - shape  
  - nulls  
  - unique values  
  - distributions  
  → continuous *before vs. after* comparison.

---

## 🧪 1) SOP: Standard Flow Applied to Every Column

The same disciplined workflow was applied column by column.

---

### 🔍 Profiling (Triage)

- Null ratio
- Number of unique values
- `value_counts`
- Extreme value lists (head / tail)

**Goal:**  
Is this column reliable?  
Is the issue a *true outlier* or a *data entry error*?

---

### 📊 Distribution Inspection (Evidence)

- Histogram
- Boxplot

Key questions:
- Is there a heavy right tail?
- Is the distribution bimodal?
- Does z-score make sense here, or is IQR safer?

---

### 🧾 Contextual Review of Extremes

- Sorted min/max values using `sort_values`
- Manual plausibility checks
- In some cases, inspected **make / model / body_type** context

---

### 🧠 Decision Rule Selection

- Impossible / invalid values → **NaN + group-wise imputation**
- Extreme but plausible values → **IQR-based drop** (especially price, mileage)
- Discrete nonsense (e.g. `gears == 0`, `owners >= 10`) → **rule-based correction / NaN / drop**
- Final stabilization → **z-style pruning** where appropriate

---

### ✅ Final Validation

- Are nulls back to zero?
- Did unique counts normalize?
- Does the distribution look stable?
- Was shape change logged?

---

## 🧩 2) Decision Tree: What We Did — and Did Not Do

Think of this as an explicit **if–then logic**.

---

### ✅ A) Signal: “Impossible Value”  
*(typo / unit error / parsing issue)*

**Example signals:**
- `engine_size = 99900`, `54009` → unit confusion
- `empty_weight = 75 kg` → physically impossible
- `co_emissions = 940` → logically implausible

**➡️ What we did:**
- Converted values to **NaN**
- Imputed using **median or mode** within  
  `make_model × body_type` groups

**➡️ What we did NOT do:**
- Did **not** apply z-score first  
  (std is already contaminated → misleading pruning)
- Did **not** use global median  
  (vehicle groups are heterogeneous → meaningless fill)

---

### ✅ B) Signal: “Heavy Tail + Naturally Extreme Feature”

**Example signals:**
- `price` and `mileage` show classic heavy-tail behavior
- Boxplots dominated by long right tails

**➡️ What we did:**
- Applied **IQR (Tukey Fence 1.5×IQR)** → drop
- For `price`, additionally applied **model-based anomaly rules first**

**➡️ What we did NOT do:**
- Did **not** default to z-score  
  (on skewed distributions, z-score can be overly aggressive or incorrect)

---

### ✅ C) Signal: “Discrete Column + Illogical Values”

**Example signals:**
- `gears = 0` → often means “unknown”
- `gears > 8` → suspicious in this dataset context
- `previous_owner >= 10` → extremely rare + quality concern

**➡️ What we did:**
- Applied **explicit domain rules**: NaN / correction / drop
- Used **mode imputation** when appropriate  
  (mode is more meaningful for discrete variables)

**➡️ What we did NOT do:**
- Did **not** treat these as statistical outliers  
  (boxplot / z-score are misleading for discrete features)

---

## ✅ 3) Quality Gates Applied at Every Step

After each cleaning action, we verified four checkpoints:

- 📐 **Shape change**  
  (How many rows / columns were affected?)
- 🕳️ **Null check**  
  (Did imputation resolve NaNs correctly?)
- 🧮 **Unique count sanity**  
  (Did discrete features normalize?)
- 📉 **Distribution stability**  
  (Were tails reduced? Boxplots interpretable?)

👉 This is why Phase 03 is **not a one-shot cleanup**,  
but an **iterative decision + validation loop**.

---

## 🧠 4) What We Explicitly Did NOT Do (By Design)

- 🚫 No fully automatic global outlier detectors  
  (Isolation Forest, LOF, etc.)  
  → Phase 03 focused on **EDA + explainable cleaning**

- 🚫 No multivariate outlier analysis  
  → Deferred to **Phase 05** via model residual diagnostics

- 🚫 No permanent winsorization or log transforms everywhere  
  → Used only for **visual comparison**, not as default data transformation

---

## 📌 Outcome: What This Methodology Achieved

- 📉 Reduced dominance of extreme values in modeling
- 🧱 Stabilized numeric feature distributions
- 🧹 Removed noise-heavy columns and duplicates
- ✅ Delivered a **clean, explainable, model-ready dataset**

