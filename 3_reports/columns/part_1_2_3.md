## A) Pipeline Kolonları (Phase 1 → Phase 3)

| Kolon | Phase 1 (Data Cleaning) | Phase 2 (Missing Values) | Phase 3 (Outliers + Final Step) | Son Durum |
|---|---|---|---|---|
| make_model | ✅ snake_case + temel text standardizasyonu (brand+model kimliği olarak kullanıldı). | 🔧 `model` düzeldikten sonra **make + model** ile yeniden oluşturuldu; `.str.title()` ile format birliği. | 🧭 Grup anahtarı olarak kullanıldı (outlier değil). | ✅ Finalde Var |
| short_description | ✅ Korundu (model/kimlik doğrulama için yardımcı text). | 🧠 Regex ile `model` kurtarmada kullanıldı; iş bitince **drop**. | — | ❌ Phase 2'de Silindi |
| make | ✅ Text temizlik/standardizasyon (brand). | 🔤 `.str.title()` ile format birliği (make_model rebuild için kullanıldı). | — | ✅ Finalde Var |
| model | ✅ Text temizlik/standardizasyon. | 🧠 Regex ile `short_description` içinden çıkarıldı ve `fillna`; kurtarılamayan az sayıda satır **drop**. | — | ✅ Finalde Var |
| location | ✅ Temizlendi/standardize edildi (string). | — | — | ✅ Finalde Var |
| price | 🔢 Numerik dönüşüm + format temizliği (€, virgül/nokta vb.). | — | 🚨 Domain filtre + **IQR (Tukey Fence)** ile uç değer satırları drop. | ✅ Finalde Var |
| body_type | ✅ Kategori temizliği/standardizasyon. | 🔤 `.str.title()` ile format birliği (gruplama için). | 🧭 Grup anahtarı olarak kullanıldı (outlier değil). | ✅ Finalde Var |
| type | ✅ Kategori temizliği/standardizasyon. | — | — | ✅ Finalde Var |
| doors | 🔢 Numerik/format kontrolü (kategori/numeric temizliği). | 🧩 Group-based **mode fill** (make_model + body_type → fallback). | 🗑 Kolon komple **drop** (katkı düşük / kararsız). | ❌ Phase 3'te Silindi |
| warranty | ✅ Temel temizlik (string). | 🧾 Rule-based: `-` → **No**, diğerleri → **Yes** (ikili sınıf). | — | ✅ Finalde Var |
| mileage | 🔢 Numerik dönüşüm + format temizliği. | 📈 `make_model + age` gruplarında **mean fill** (segment ortalaması). | 🚨 `> 1,000,000` drop + **IQR (Tukey)** ile uçlar drop. | ✅ Finalde Var |
| gearbox | ✅ Kategori temizliği/standardizasyon. | 🧩 Group-based **mode fill**. | — | ✅ Finalde Var |
| fuel_type | ✅ Kategori temizliği/standardizasyon. | 🧩 Group-based **mode fill** (make_model + gearbox) + 1 manuel düzeltme (tek kayıt). | — | ✅ Finalde Var |
| seller | ✅ Kategori temizliği/standardizasyon. | — | — | ✅ Finalde Var |
| seats | 🔢 Numerik/format kontrolü. | 🧩 Group-based **mode fill**. | 🗑 Kolon komple **drop**. | ❌ Phase 3'te Silindi |
| engine_size | 🔢 Numerik dönüşüm + format temizliği. | 🧩 `-` → NaN; group-based **mode fill** (make_model + body_type). | 🚨 Anormal set → NaN; sonra **mode fill**; kalan uçlar için z-score drop. | ✅ Finalde Var |
| gears | 🔢 Numerik/format temizliği. | 🧩 `-` → NaN; çok seviyeli group-based **mode fill** (make_model/body_type/gearbox → fallback). | 🚨 `0` veya `>8` → NaN + mode fill; `==2` satırları drop. | ✅ Finalde Var |
| co_emissions | 🔢 Numerik dönüşüm + format temizliği. | ⚡ Electric özel kontrol + segment **median fill** (çok seviyeli fallback). | 🚨 Aşırı değerler → NaN; **median fill**; log1p inceleme; z-score drop. | ✅ Finalde Var |
| drivetrain | ✅ Kategori temizliği/standardizasyon. | 🧩 Group-based **mode fill**. | — | ✅ Finalde Var |
| cylinders | 🔢 Numerik/format temizliği. | 🧩 Mode fill yapıldı; sonra düşük katkı/redundant görüldü → **drop**. | — | ❌ Phase 2'de Silindi |
| empty_weight | 🔢 Numerik dönüşüm + format temizliği. | 🧩 Group-based **mode fill**. | 🚨 `>4000` ve {75, 525} → NaN; sonra mode fill. | ✅ Finalde Var |
| full_service_history | ✅ Kategori temizliği/standardizasyon. | — | — | ✅ Finalde Var |
| upholstery | ✅ Kategori temizliği/standardizasyon. | 🪑 Kategori birleştirme (Velour→Cloth vb.); `Other`→NaN; group ffill/bfill. | — | ✅ Finalde Var |
| previous_owner | 🔢 Numerik/format temizliği. | 🔁 `age` içinde ffill/bfill (propagation). | 🚨 `>=10` satırlar drop. | ✅ Finalde Var |
| energy_efficiency_class | ✅ Kategori temizliği (string). | 🧩 Group-based **mode fill** (`make_model + age` → fallback). | — | ✅ Finalde Var |
| extras | 🧾 List/text alanı temizlendi (stringleştirme). | 🧩 Group-based **mode fill**. | — | ✅ Finalde Var |
| age | 🧠 **Feature Engineering:** `age = 2022 - first_registration` | 🧓 Domain rule: `mileage < 10000` ise eksik age → `0` (new car). | 🚨 `age < 0` veya `age > 20` satırlar drop. | ✅ Finalde Var |
| power_kW | 🧠 **Feature Engineering:** `power` içinden regex ile `power_kW` ve `power_hp` çıkarıldı; numeric. | 🧩 `-`→NaN; group-based **mode fill** (`make_model + body_type`). | 🚨 Düşük frekanslı kW değerleri → NaN; segment **median fill**; z-score drop. | ✅ Finalde Var |
| power_hp | 🧠 `power` içinden çıkarıldı (numeric). | 🧩 Group-based **mode fill**; sonra `power_kW` ile redundant → **drop**. | — | ❌ Phase 2'de Silindi |
| cons_avg | 🧠 **Feature Engineering:** `fuel_consumption` içinden `cons_avg` çıkarıldı; numeric. | ⚡ Electric için sabit değer; kalanlar için segment **median fill**. | 🚨 `>=20` → NaN; median fill; z-score drop. | ✅ Finalde Var |
| cons_city | 🧠 `fuel_consumption` içinden çıkarıldı. | 🗑 `cons_avg` seçildiği için redundant → **drop**. | — | ❌ Phase 2'de Silindi |
| cons_country | 🧠 `fuel_consumption` içinden çıkarıldı. | 🗑 `cons_avg` seçildiği için redundant → **drop**. | — | ❌ Phase 2'de Silindi |
| comfort_convenience | 🧾 List/text temizliği (stringleştirme). | 🧩 Mode fill → **Package feature** üretildi → ham kolon **drop**. | — | ❌ Phase 2'de Silindi |
| entertainment_media | 🧾 List/text temizliği (stringleştirme). | 🧩 Mode fill → **Package feature** üretildi → ham kolon **drop**. | — | ❌ Phase 2'de Silindi |
| safety_security | 🧾 List/text temizliği (stringleştirme). | 🧩 Mode fill → **Package feature** üretildi → ham kolon **drop**. | — | ❌ Phase 2'de Silindi |
| comfort_convenience_Package | — | 🧪 Feature Engineering: comfort text → **Standard / Premium / Premium Plus** paket seviyesi. | — | ✅ Finalde Var |
| entertainment_media_Package | — | 🧪 Feature Engineering: media text → **Standard Media / Media Plus**. | — | ✅ Finalde Var |
| safety_security_Package | — | 🧪 Feature Engineering: safety text → **Standard / Premium / Premium Plus**. | — | ✅ Finalde Var |

---

## B) Geçici Helper Kolonlar

| Kolon | Phase 1 (Data Cleaning) | Phase 2 (Missing Values) | Phase 3 (Outliers + Final Step) | Son Durum |
|---|---|---|---|---|
| extracted_models (helper) | — | 🧠 Regex extraction sonucu geçici kolon; `model` doldurma sonrası **drop**. | — | ❌ Phase 2'de Silindi |
| modified_make_model (helper) | — | 🔧 make+model ile geçici kimlik; `make_model` güncelleme sonrası **drop**. | — | ❌ Phase 2'de Silindi |

---

## C) Phase 1'de Silinen Kolonlar (Raw-only / High Missing / Kapsam Dışı)

| Kolon | Phase 1 (Data Cleaning) | Phase 2 (Missing Values) | Phase 3 (Outliers + Final Step) | Son Durum |
|---|---|---|---|---|
| availability | 🗑 Çok yüksek missing / düşük kullanım (>%80 NaN) → toplu **drop**. | — | — | ❌ Phase 1'de Silindi |
| available_from | 🗑 Çok yüksek missing / düşük kullanım (>%80 NaN) → toplu **drop**. | — | — | ❌ Phase 1'de Silindi |
| battery_ownership | 🗑 Çok yüksek missing / düşük kullanım (>%80 NaN) → toplu **drop**. | — | — | ❌ Phase 1'de Silindi |
| co_efficiency | 🗑 Çok yüksek missing / düşük kullanım (>%80 NaN) → toplu **drop**. | — | — | ❌ Phase 1'de Silindi |
| co_emissions_wltp | 🗑 Çok yüksek missing / düşük kullanım (>%80 NaN) → toplu **drop**. | — | — | ❌ Phase 1'de Silindi |
| colour | 🗑 Düşük değer / redundant / proje kapsamı dışı → **drop**. | — | — | ❌ Phase 1'de Silindi |
| country_version | 🗑 Düşük değer / redundant / proje kapsamı dışı → **drop**. | — | — | ❌ Phase 1'de Silindi |
| desc | 🗑 Düşük değer / redundant / proje kapsamı dışı → **drop**. | — | — | ❌ Phase 1'de Silindi |
| electric_range_wltp | 🗑 Çok yüksek missing / düşük kullanım (>%80 NaN) → toplu **drop**. | — | — | ❌ Phase 1'de Silindi |
| emission_class | 🗑 Düşük değer / redundant / proje kapsamı dışı → **drop**. | — | — | ❌ Phase 1'de Silindi |
| emissions_sticker | 🗑 Düşük değer / redundant / proje kapsamı dışı → **drop**. | — | — | ❌ Phase 1'de Silindi |
| first_registration | 🧠 Kaynak kolon: yeni feature üretildi ve sonra **drop**. | — | — | ❌ Phase 1'de Silindi |
| fuel_consumption | 🧠 Kaynak kolon: yeni feature üretildi ve sonra **drop**. | — | — | ❌ Phase 1'de Silindi |
| fuel_consumption_wltp | 🗑 Çok yüksek missing / düşük kullanım (>%80 NaN) → toplu **drop**. | — | — | ❌ Phase 1'de Silindi |
| general_inspection | 🗑 Düşük değer / redundant / proje kapsamı dışı → **drop**. | — | — | ❌ Phase 1'de Silindi |
| last_service | 🗑 Çok yüksek missing / düşük kullanım (>%80 NaN) → toplu **drop**. | — | — | ❌ Phase 1'de Silindi |
| last_timing_belt_change | 🗑 Çok yüksek missing / düşük kullanım (>%80 NaN) → toplu **drop**. | — | — | ❌ Phase 1'de Silindi |
| manufacturer_colour | 🗑 Düşük değer / redundant / proje kapsamı dışı → **drop**. | — | — | ❌ Phase 1'de Silindi |
| model_code | 🗑 Düşük değer / redundant / proje kapsamı dışı → **drop**. | — | — | ❌ Phase 1'de Silindi |
| non_smoker_vehicle | 🗑 Düşük değer / redundant / proje kapsamı dışı → **drop**. | — | — | ❌ Phase 1'de Silindi |
| offer_number | 🗑 Düşük değer / redundant / proje kapsamı dışı → **drop**. | — | — | ❌ Phase 1'de Silindi |
| other_fuel_types | 🗑 Çok yüksek missing / düşük kullanım (>%80 NaN) → toplu **drop**. | — | — | ❌ Phase 1'de Silindi |
| paint | 🗑 Düşük değer / redundant / proje kapsamı dışı → **drop**. | — | — | ❌ Phase 1'de Silindi |
| power | 🧠 Kaynak kolon: yeni feature üretildi ve sonra **drop**. | — | — | ❌ Phase 1'de Silindi |
| power_consumption | 🗑 Çok yüksek missing / düşük kullanım (>%80 NaN) → toplu **drop**. | — | — | ❌ Phase 1'de Silindi |
| power_consumption_wltp | 🗑 Çok yüksek missing / düşük kullanım (>%80 NaN) → toplu **drop**. | — | — | ❌ Phase 1'de Silindi |
| production_date | 🧠 Kaynak kolon: yeni feature üretildi ve sonra **drop**. | — | — | ❌ Phase 1'de Silindi |
| taxi_or_rental_car | 🗑 Çok yüksek missing / düşük kullanım (>%80 NaN) → toplu **drop**. | — | — | ❌ Phase 1'de Silindi |
| upholstery_colour | 🗑 Düşük değer / redundant / proje kapsamı dışı → **drop**. | — | — | ❌ Phase 1'de Silindi |
