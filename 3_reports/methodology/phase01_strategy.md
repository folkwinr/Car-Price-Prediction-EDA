# 🧪 Part-01 Methodology (Data Cleaning) — Step-by-Step (AutoScout24)

> Bu bölümde hedefimiz: **raw JSON → temiz, tutarlı, analiz/modellemeye hazır bir tablo** üretmekti.  
> Stratejimiz “önce genel temizlik + kalite kontrol, sonra kolon-kolon (column-wise) dönüşüm, sonra feature engineering” şeklindeydi.

---

## 🧭 0) Başlangıç Mantığı: Biz neyi çözmeye çalıştık?
Raw ilan verilerinde tipik sorunlar vardı:
- 🧾 Kolon adları karmaşık / newline / özel karakter (schema dağınıklığı)
- 🔢 Sayısal değerler **metin** içinde (price, mileage, consumption, power…)
- 🧩 Bazı hücreler **list** (donanım grupları, bazı kategorikler)
- 🕳️ Çok fazla missing value (özellikle WLTP / EV alanları)
- 🔁 Duplicate riski (scrape datada sık görülebilir)

Bu yüzden karar ağacımız hep şuydu:
- **Önce görünürlük:** “Ne var, ne kadar boş, format nasıl?”
- **Sonra temizlik:** “Şema + noise removal + type conversion”
- **Sonra anlam:** “Feature engineering + kategorik sadeleştirme”
- **En son kontrol:** “Data quality gate”

---

## 1) 🧰 Genel Hazırlık (General Setup)
### 1.1 📥 Load + Copy (Raw veriyi koruduk)
- ✅ `pd.read_json(...)` ile raw veriyi aldık.
- ✅ `df = df0.copy()` yaptık.
- **Neden?** Raw veri bozulmasın, her adımı geri kontrol edebilelim.

### 1.2 🔍 Hızlı genel özet (skimpy + hızlı EDA araçları)
- ✅ `skimpy` (ve benzeri hızlı özet) ile:
  - kolon tipleri
  - missing oranları
  - temel dağılım sinyali
  hızlıca görüldü.
- ✅ Kendi fonksiyonlarımızla (örn. `first_looking`) kolon bazlı:
  - null yüzdesi / null sayısı
  - unique sayısı
  - value_counts
  kontrol edildi.

**Buradaki düşünce:**
> “Önce problemi gör. Formatı anlamadan dönüşüm yaparsan parsing hatası büyür.”

---

## 2) 🧹 Genel Temizlik (Global Cleaning Rules)
### 2.1 🏷️ Kolon isim standardizasyonu (Schema normalize)
- ✅ `to_snake_case()` ile kolon adlarını standard yaptık:
  - newline / boşluk / özel karakter temizliği
  - lowercase + underscore
- **Neden?** Kod güvenliği + okunabilirlik + GitHub kalitesi.

### 2.2 🗑️ Tamamen boş satırları attık
- ✅ `dropna(how="all")`
- **Neden?** Bilgi taşımayan satır analizi kirletir.

### 2.3 🕳️ Çok boş kolonları eledik (Missing threshold)
- ✅ Missing oranlarına baktık (`df_nans` / `show_missing_values`)
- ✅ Kural: **>%80 missing olan kolonlar drop**
- **Neden?**
  - Part-02’de doldurmak için bile veri yok
  - dataset’i şişiriyor, sinyal yerine gürültü yaratıyor

> Karar noktası:
> - Eğer kolon **>%80 missing** ise → **drop**
> - Eğer kolon orta seviyede missing ise → **Part-02’ye bırak**
> - Eğer kolon “core” ise (price/mileage gibi) → kesinlikle tutulur, sonra doldurulur

### 2.4 🔁 Duplicate kontrolü
- ✅ `duplicated()` ile kontrol etmek istedik.
- 🧩 List tipler sorun çıkarabildiği için:
  - `df.astype(str).duplicated()` gibi bir workaround ile mantıksal kontrol yaptık.
- **Neden?** Scrape datada aynı ilan/benzer kayıt tekrar edebilir.

---

## 3) 🧩 Kolon-Kolon Temizleme Stratejisi (Column-wise Cleaning Strategy)
Her kolonda şu 3 soruyla ilerledik:

### ✅ Soru-1: Bu kolonun “formatı” ne?
- Eğer **list** ise → list handling
- Eğer **numeric-like text** ise → regex + numeric conversion
- Eğer **category/text** ise → strip/normalize/mapping
- Eğer **free-text (desc)** ise → bu fazda drop (NLP yok)

### ✅ Soru-2: Bu kolon “işe yarıyor mu”?
- Core feature mı? (price, mileage, age, power, fuel…)
- Çok boş mu?
- ID/leakage riski var mı? (Offer number)

### ✅ Soru-3: Bu kolondan “daha iyi bir feature” üretebilir miyiz?
- power → kW + hp
- fuel_consumption → avg/city/country
- first_registration → age

---

## 4) 🧷 List Handling (List gelen kolonlarda karar ağacı)
Raw data içinde bazı kolonlar list gelebiliyordu.

### 4.1 ✅ Eğer list “tek elemanlı” ise (en sık durum)
- Uyguladığımız yol:  
  - `x[0] if isinstance(x, list) else x`
- **Neden?** Satır sayısını değiştirmeden scalar değere ineriz.

### 4.2 ⚠️ `.explode()` kullandığımız yerler (riskli ama pratik)
- Bazı kolonlarda: `explode().str.strip(...)` yaptık.
- **Bu ne zaman iyi?**
  - list’in çoğunlukla tek elemanlı olduğunu bildiğimizde
- **Risk:**
  - list >1 elemanlıysa satır sayısını artırır → veri bozulabilir

> Bu yüzden strateji:  
> - “Eminsek” explode  
> - “Emin değilsek” ilk elemanı al (daha güvenli)

### 4.3 🧩 Equipment kolonları (list → okunabilir text)
- `comfort / entertainment / safety / extras` gibi list kolonlarda:
  - `", ".join(list)` ile tek string yaptık.
- **Neden?** Part-01’de hedef: **okunabilirlik + stabil dataset**
- **Not:** Modelleme için ideal format değil; ileride:
  - `equipment_count`
  - `has_feature_X` (0/1 flag)
  gibi encode edilir.

---

## 5) 🔡 Regex ile Sayısallaştırma (Text → Numeric Parsing)
Bu bölüm Part-01’in “çekirdek motoru” oldu.

### 5.1 💰 Price
- Baktık: değerler metin + para birimi/ayırıcı içeriyor.
- Uyguladık:
  - regex ile sayı çekme (`extract`)
  - ayırıcı temizleme (`,` gibi)
  - `astype(float)` ile numeric yapma

**Neden?** price numeric olmadan EDA/outlier/model olmaz.

### 5.2 🛣️ Mileage
- Baktık: “km” ve ayırıcılar var.
- Uyguladık:
  - separator temizleme
  - regex ile digit extract
  - numeric conversion

### 5.3 ⚙️ Engine/weight/gear/cylinders gibi alanlar
- Baktık: numeric-like string
- Uyguladık:
  - `extract('(\d+)')` yaklaşımı
  - numeric conversion

> Genel kural:
> - metinde sayı varsa → regex ile ayıkla → numeric'e çevir  
> - dönüşümde hata riski varsa → Part-02’de missing olarak ele al

---

## 6) 🧠 Feature Engineering (Özellik türetme) — “Temizle + Güçlendir”
Bu adım “sadece temizleme” değil, veriyi **daha faydalı** hale getirme adımıydı.

### 6.1 📅 First registration → Age
- Baktık: first_registration tarih formatı karışabiliyor ve model için “age” daha iyi.
- Uyguladık:
  - yıl extract (son 4 karakter gibi)
  - `age = reference_year - year`
- Sonra:
  - `first_registration` ve `production_date` gibi kaynak kolonları drop ettik (redundant)

### 6.2 ⚙️ Power → power_kW + power_hp
- Baktık: power metin içinde iki birim içeriyor (kW/hp).
- Uyguladık:
  - list ise ilk eleman
  - regex ile iki değeri çıkarma
  - iki yeni numeric kolon üretme
- Sonra:
  - kaynak `power` drop (artık gereksiz)

### 6.3 ⛽ Fuel consumption → cons_avg / cons_city / cons_country
- Baktık: consumption alanı tek kolonda karmaşık bir yapı.
- Uyguladık:
  - helper fonksiyonlarla doğru parçayı seçme
  - regex ile numeric extract
  - `cons_avg`, `cons_city`, `cons_country` üretme
- Sonra:
  - `fuel_consumption` drop

---

## 7) 🧩 Categorical Normalization (Kategorik sadeleştirme)
### 7.1 ⛽ Fuel type mapping
- Baktık: fuel_type çok farklı yazımlarla geliyor.
- Uyguladık:
  - `/` split (ilk parçayı alma)
  - mapping fonksiyonu ile benzerleri aynı grupta toplama
- **Neden?** Çok fazla kategori = dağınık analiz. Daha az kategori = daha güçlü sinyal.

### 7.2 🌿 Emission / Efficiency gruplama
- Baktık: emission class ve efficiency class çok varyantlı.
- Uyguladık:
  - normalize eden fonksiyonlarla gruplama
- Karar:
  - bazılarını sonradan drop ettik (bu faz için gerekli görmedik)

---

## 8) 🗑️ Drop Stratejisi (Neyi neden attık?)
### 8.1 🧾 Free-text
- `desc` gibi uzun metinler:
  - NLP yapmayacağımız için drop

### 8.2 🆔 ID / leakage
- `offer_number`:
  - modelin “ezberlemesine” sebep olabileceği için drop

### 8.3 🕳️ Çok boş kolonlar
- WLTP/EV alanlarının çoğu:
  - >80 missing → drop

### 8.4 🔁 Redundant (türetilen feature sonrası)
- `power` → split sonrası drop
- `fuel_consumption` → cons_* sonrası drop
- `first_registration` → age sonrası drop

---

## 9) ✅ Data Quality Gates (Son Kontroller)
Part-01 sonunda şunları kontrol ettik:
- 🧪 kolonların dtype durumu (numeric olması gerekenler numeric mi?)
- 🕳️ missing durum raporu (Part-02’ye hazırlık)
- 🔁 duplicate kontrol çıktısı (tam silme kararı sonraki aşamaya bırakılabilir)
- 📌 temel mantık kontrolleri (negatif km/fiyat gibi anormallikler Part-03’e not edilir)

---

## 🏁 Çıktı: Part-01 sonunda elimizde ne var?
- ✅ Standard kolon isimleri (snake_case)
- ✅ Core kolonlar numeric ve analiz-ready:
  - price, mileage, age, power_kW/hp, cons_*
- ✅ Donanım kolonları okunabilir formda
- ✅ Aşırı boş / düşük değerli / ID kolonları temizlenmiş
- ✅ Part-02 (missing) ve Part-03 (outlier) için sağlam zemin

---

## 🔥 Mini “Decision Log” (Kısa)
- **Missing >80%** → drop  
- **List field** → (eminsek) explode, (emin değilsek) first element  
- **Text-number** → regex extract + numeric conversion  
- **Better feature possible** → create feature, then drop source column  
- **Free text / ID** → drop (bu fazda)
