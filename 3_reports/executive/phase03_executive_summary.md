██████████████████████████████████████████████████████████████████████████████
PHASE 3 — EXECUTIVE SUMMARY
Outlier Handling & Data Quality Stabilization (Scout 2022)
██████████████████████████████████████████████████████████████████████████████

OVERVIEW
Phase 3 focuses on making the dataset model-ready by reducing noise from data entry errors,
extreme outliers, and duplicate records—especially those that distort price modeling.
The approach is not “drop rows everywhere.” Instead, when a problem is localized to a single
feature value, we prefer preserving the row and correcting the value via NaN + group-wise
imputation. This phase delivers more stable feature distributions and stronger domain
consistency, while documenting key multicollinearity risks for the next phase.

SCOPE & DELIVERABLES
Included
- Target sanitation for price (manual anomaly cleanup + distribution-based trimming)
- Domain validity rules (impossible/suspicious values -> NaN or drop)
- Outlier handling via:
  (1) IQR / Tukey Fence
  (2) Median-centered z-like thresholding (z < 3)
- Duplicate removal
- Post-cleanup verification (distribution plots, null checks, correlation/multicollinearity scan)

Delivered Output
- Cleaned dataset suitable for modeling: 21,769 rows × 28 columns
- Two low-trust / low-signal columns removed: doors, seats
- Clean intermediate outputs enabling downstream encoding and modeling

IMPACT SUMMARY (KPIs)
- Start: 28,624 rows × 30 columns
- End:   21,769 rows × 28 columns
- Net row reduction: 6,855 (~23.95%)
- Net column reduction: 2 (doors, seats)

Largest row reductions (drivers of phase behavior)
- price IQR trimming:               -1,914 rows
- age domain cutoff (>20 or <0):    -1,242 rows
- duplicate removal:                -1,470 rows
- power_kW z-like outlier drop:       -601 rows

CORE QUALITY ARCHITECTURE (3-LAYER STRATEGY)
1) DOMAIN RULES (Validity First)
   Goal: enforce physical/business plausibility before statistical trimming.
   Examples: gears==0 is invalid -> NaN; mileage>1,000,000 is extreme -> drop; age<0 -> drop.

2) DISTRIBUTION RULES (IQR / Tukey Fence)
   Goal: systematically remove distribution-breaking extremes.
   Applied notably to price and mileage to prevent heavy-tailed distortion in modeling.

3) ROBUST-LEANING THRESHOLDING (Median-centered z-like filter, z<3)
   Goal: remove tail observations not captured by hard rules.
   Applied to engine_size, co_emissions, cons_avg, and power_kW.

NOTE ON ROBUSTNESS
The z-like method uses median as center but still uses standard deviation as scale, which is
less robust than a true “modified z-score” (MAD-based). This is flagged for improvement in
Phase 4.

KEY DECISIONS (BUSINESS-READY RATIONALE)

1) PRICE (Target) — “Protect model learnability”
- Step 1: targeted manual removal for extreme make/model price anomalies
- Step 2: IQR/Tukey trimming to reduce heavy-tail dominance
Why: extreme target values can dominate loss functions and destabilize training.
Trade-off: may under-represent ultra-luxury/collector segments.

2) GEARS — “Statistical outlier ≠ domain outlier”
- Verified Electric vehicles commonly have gears=1; retained as valid despite appearing
  as a boxplot outlier.
- Converted invalid/unsupported values (gears==0 or gears>8) to NaN, then imputed via
  make_model + body_type using mode (609 values recovered).
- Dropped one clearly inconsistent gears==2 record (1 row).
Why: gears is numeric-looking but categorical in nature; mode is the safest imputation.
Outcome: minimal row loss, strong consistency gain.

3) EMPTY_WEIGHT — “Don’t burn rows; fix the cell”
- Identified physically implausible extremes (e.g., 15590, 11246) and specific absurd entries
  (e.g., 75, 525). Converted to NaN rather than dropping rows.
- Imputed using make_model + body_type with mode (3 values corrected).
Why: the row may contain valuable signal in other features; the error is localized.

4) CO_EMISSIONS — “Evaluate alternatives before committing”
- Reviewed winsorization and log-transform plots to assess whether transformation/capping
  could manage the heavy tail without deletion.
- Marked clearly suspicious values (940/910/420/414) as NaN, then imputed via group median.
- Applied z-like thresholding (z<3) to remove remaining tail outliers (~200 rows).
Why: some values behave like data quality errors rather than merely “skew.”

QUALITY CHECKS AFTER CLEANUP
- Distribution stabilization: histograms/boxplots became interpretable; extreme scale
  distortions were reduced in empty_weight, co_emissions, cons_avg, power_kW.
- Multicollinearity scan (corr ≥ 0.6) highlighted expected relationships:
  age ↔ mileage, co_emissions ↔ cons_avg, engine_size ↔ power_kW, empty_weight ↔ power_kW.
Business interpretation: these features may carry overlapping signal; address via selection,
regularization, or grouping in Phase 4.

RISKS & EXECUTIVE WARNINGS
- Segment truncation risk: dropping age>20 removes classic/youngtimer dynamics.
  Acceptable only if the business scope is “mainstream used cars.”
- Performance-segment risk: rare kW handling + tail trimming may under-represent high-output
  variants.
- Rule-based standardization risk: model-specific rules improve consistency but may hide true
  trim/year variability.

PHASE 4 RECOMMENDATIONS (NEXT STEPS)
1) Robust outlier metric: replace std-scale z-like filter with MAD-based modified z-score.
2) Group-wise thresholds: consider make/model-based bands for price and mileage to avoid
   unfair trimming of premium segments.
3) Production-grade pipeline: implement cleaning + imputation + encoding in a strict
   fit-on-train / transform-on-test workflow (Pipeline/ColumnTransformer).
4) Governance: maintain a rule registry (why/impact/count) for auditability.
5) Bias review: quantify distribution shifts caused by age cutoff and rare power_kW handling.

ONE-LINE EXECUTIVE CONCLUSION
Phase 3 materially improved data reliability and model readiness by removing extreme
distortions and duplicates while preserving rows where possible via targeted correction;
however, age cutoffs and performance-tail handling require explicit bias/segment validation
in Phase 4.
██████████████████████████████████████████████████████████████████████████████
