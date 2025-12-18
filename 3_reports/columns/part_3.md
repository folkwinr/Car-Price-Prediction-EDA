# 🧾 Phase 03 — Column-by-Column Actions (Outlier Handling)

| Column | 🔍 Observed Signal | 🛠️ Decision Taken | ⚙️ Method Applied | 📉 Impact / Outcome |
|------|------------------|------------------|------------------|--------------------|
| 🎯 price | Extreme prices in some make/model groups + heavy-tail distribution | Drop anomalies first, then trim outliers | 1) Model-based threshold drop  2) Tukey Fence (1.5×IQR) | (28,624,30) → (28,617,30) −7 → (26,703,30) −1,914 (**Total −1,921**) |
| 🚪 doors | Illogical/rare values (1, 6 doors) + low reliability | Convert outliers to NaN, impute, then drop column | replace([1,6], NaN) → mode fill (make_model×body_type) → drop(`doors`) | NaN: 7; column dropped → (26,703,30) → (26,703,29) |
| 🛣️ mileage | >1,000,000 clearly invalid; remaining distribution heavy-tail | Drop obvious errors, then IQR trimming | mileage > 1e6 drop → Tukey Fence | (26,703,29) → (26,699,29) −4 → (26,115,29) −584 |
| 💺 seats | Low signal-to-noise ratio; weak reliability and usefulness | Drop column entirely | drop(`seats`) | (26,115,29) → (26,115,28) |
| 🛠️ engine_size | Impossible values due to unit/typo issues (extreme, nonsensical) | Set invalid values to NaN, group-impute, final pruning | Invalid list → NaN (15) → mode fill (make_model×body_type) → z-score pruning | (26,115,28) → (25,446,28) −669 |
| ⚙️ gears | 0 (unknown) + >8 suspicious; special model fix; one invalid value | NaN + mode impute; drop incompatible record | Mustang domain fix → (0 or >8)=NaN (609) → mode fill → gears==2 drop | (25,446,28) → (25,445,28) −1 |
| 🧱 empty_weight | >4,000 extreme; 75 and 525 physically impossible | Convert to NaN and impute via mode | >4,000 and [75,525] → NaN (3) → mode fill | No row drop (shape unchanged) |
| 🌫️ co_emissions | Candidates like 940/910/420/414; skewed distribution | NaN + median fill; final z-score pruning | [940,910,420,414] → NaN (4) → median fill → z-score pruning | (25,445,28) → (25,245,28) −200 |
| ⛽ cons_avg | ≥20 L/100km suspicious; extreme values (e.g. 99.9) | NaN + median fill; final z-score pruning | cons_avg ≥ 20 → NaN (12) → median fill → z-score pruning | (25,245,28) → (25,088,28) −157 |
| 👤 previous_owner | Discrete feature; ≥10 extremely rare + quality concern | Direct drop (discrete policy) | previous_owner ≥ 10 drop | (25,088,28) → (25,082,28) −6 |
| 🕰️ age | Negative values impossible; >20 outside project segment | Hard policy: drop | (age < 0) OR (age > 20) drop | (25,082,28) → (23,840,28) −1,242 |
| ⚡ power_kW | Very rare values (count < 10) may be typo/parse; highly influential feature | Rare → NaN, median fill, z-score pruning | value_counts < 10 → NaN (257) → median fill → z-score pruning | (23,840,28) → (23,239,28) −601 |

---

## 📌 Phase 03 — Total Impact (Outlier Block)

- **Start:** (28,624 × 30)
- **After outlier handling:** (23,239 × 28)  
  → −5,385 rows, −2 columns (`doors`, `seats`)
- **After deduplication:** (21,769 × 28)  
  → −1,470 rows
- **Export-ready (location removed):** (21,769 × 27)

