# 📘 Data Dictionary — Raw Dataset Columns (AutoScout24)

> **Source:** `as24_cars.json` (raw listings)  
> **Total columns:** 58  
> **Note:** Raw pandas dtype çoğunlukla `object` olur; aşağıda “Raw format/type” kısmı pratikte görülen formatı anlatır.

---

## 🧾 A) Listing Identity & Seller (İlan kimliği ve satıcı)
| Column | Raw format/type | Target type | Description |
|---|---|---|---|
| `make_model` | string | string/category | Marka + model birleşimi (segment analizi için çok güçlü). |
| `short_description` | string | string | İlanın kısa başlığı/özeti. |
| `make` | string | string/category | Marka (brand). |
| `model` | string | string/category | Model adı. |
| `location` | string | string/category | Konum (şehir/bölge). |
| `Offer number` | string/id-like | string | İlan/teklif numarası (ID). Genelde modelde kullanılmaz (leakage riski). |
| `seller` | string/category | category | Satıcı tipi (dealer/private benzeri). |

---

## 💰 B) Price & Usage (Fiyat ve kullanım)
| Column | Raw format/type | Target type | Description |
|---|---|---|---|
| `price` | numeric-like string (para birimi/separator içerebilir) | numeric (float/int) | İlan fiyatı. Parsing ile sayıya çevrilir. |
| `Mileage` | numeric-like string (km + separator olabilir) | numeric (int) | Kilometre. Temizlenip sayıya çevrilir. |

---

## 🗓️ C) Dates & Availability (Tarih ve uygunluk)
| Column | Raw format/type | Target type | Description |
|---|---|---|---|
| `First registration` | date/year-like string | int (year) / derived `age` | İlk tescil tarihi/yılı. Çoğunlukla yıl çıkarılır ve `age` üretilir. |
| `Production date` | date/year-like string | int/year or dropped | Üretim tarihi (çok boş olabilir; bazen drop edilir). |
| `Available from` | date-like string | date/string | Ne zamandan itibaren uygun (çoğunlukla çok boş). |
| `Availability` | string/category | category | Uygunluk durumu (çoğunlukla çok boş). |

---

## 🚗 D) Body & Interior/Exterior (Gövde ve iç/dış görünüm)
| Column | Raw format/type | Target type | Description |
|---|---|---|---|
| `Body type` | string/category | category | Kasa tipi (SUV, Sedan, Hatchback…). |
| `Type` | string/category | category | İlanın verdiği tip/versiyon bilgisi. |
| `Doors` | numeric-like string | int | Kapı sayısı. |
| `Seats` | numeric-like string | int | Koltuk sayısı. |
| `Colour` | string/category | category | Genel dış renk. |
| `Paint` | string/category | category | Boya tipi (metalik/solid vb.). |
| `Manufacturer colour` | string | string/category | Üretici renk adı (OEM color). |
| `Upholstery` | string/category | category | Döşeme tipi (kumaş/deri vb.). |
| `Upholstery colour` | string/category | category | Döşeme rengi. |

---

## ⚙️ E) Powertrain & Technical Specs (Motor, aktarma, teknik)
| Column | Raw format/type | Target type | Description |
|---|---|---|---|
| `Power` | string (kW/hp birlikte gelebilir) / bazen list | numeric split: `power_kW`, `power_hp` | Güç bilgisi; genelde kW ve hp ayrıştırılır. |
| `Engine size` | numeric-like string | numeric | Motor hacmi (format değişebilir; sayıya çevrilir). |
| `Cylinders` | numeric-like string | int | Silindir sayısı. |
| `Gearbox` | string/category | category | Şanzıman tipi (Manual/Automatic). |
| `Gears` | numeric-like string | int | Vites sayısı. |
| `Drivetrain` | string/category | category | Çekiş (FWD/RWD/AWD). |
| `Empty weight` | numeric-like string | numeric | Boş ağırlık (çoğunlukla kg). |

---

## ⛽ F) Fuel, Consumption & EV Fields (Yakıt, tüketim, elektrik)
| Column | Raw format/type | Target type | Description |
|---|---|---|---|
| `Fuel type` | string/category | category | Ana yakıt türü (Benzin/Dizel/Elektrik/Hibrit…). |
| `Other fuel types` | string/category | category | Ek/alternatif yakıt türleri (çoğunlukla boş). |
| `Fuel consumption` | mixed string / bazen nested yapı | numeric features (`cons_avg`, `cons_city`, `cons_country`) | Tüketim alanı; genelde parçalanıp ayrı kolonlara ayrılır. |
| `Fuel consumption (WLTP)` | numeric-like string | numeric | WLTP tüketim (çoğunlukla boş). |
| `Power consumption` | numeric-like string | numeric | Elektrik tüketimi (EV/Hybrid için; çoğunlukla boş). |
| `Power consumption (WLTP)` | numeric-like string | numeric | WLTP elektrik tüketimi (çok boş). |
| `Electric Range (WLTP)` | numeric-like string | numeric | WLTP menzil (çok boş). |
| `Battery Ownership` | string/category | category | Batarya mülkiyeti (owned/leased vb.; genelde boş). |

---

## 🌿 G) Emissions & Efficiency (Emisyon ve verimlilik)
| Column | Raw format/type | Target type | Description |
|---|---|---|---|
| `CO₂-emissions` | numeric-like string | numeric | CO₂ emisyon (genelde g/km). |
| `CO₂-emissions (WLTP)` | numeric-like string | numeric | WLTP CO₂ emisyon (çok boş). |
| `CO₂-efficiency` | string/category | category | CO₂ verimlilik etiketi/sınıfı (format değişebilir). |
| `Energy efficiency class` | string/category | category | Enerji verimlilik sınıfı (A/B/C...). |
| `Emission class` | string/category | category | Emisyon sınıfı (Euro 5/6 gibi). |
| `Emissions sticker` | string/category | category | Emisyon/çevre etiketi (ülkeye göre). |

---

## 🧰 H) Service, Inspection & History (Servis, muayene, geçmiş)
| Column | Raw format/type | Target type | Description |
|---|---|---|---|
| `Warranty` | string/category | category/bool | Garanti bilgisi (var/yok/süre). |
| `Full service history` | string/category | bool/category | Tam servis geçmişi bilgisi. |
| `Last service` | date-like string | date/string | Son servis tarihi (çoğunlukla boş). |
| `General inspection` | date-like / string | date/string/category | Genel muayene/inspection bilgisi. |
| `Previous owner` | numeric-like string | int | Önceki sahip sayısı (parse edilip sayıya çevrilebilir). |
| `Non-smoker vehicle` | bool-like string | bool/category | Sigara içilmemiş bilgisi. |
| `Last timing belt change` | date-like / string | date/string | Triger kayışı değişim bilgisi (çok boş). |
| `Taxi or rental car` | bool-like string | bool/category | Taksi/kiralama geçmişi (çok boş). |
| `Country version` | string/category | category | Ülke versiyonu (araç spec’i). |
| `Model code` | string/id-like | string | Model kodu (üretici/model kodu; bazen çok boş). |

---

## 🧩 I) Equipment Groups (Donanım paketleri — list alanlar)
> Bu 4 kolonun raw isminde başta/sonda `\n` karakterleri bulunur.

| Column | Raw format/type | Target type | Description |
|---|---|---|---|
| `\nComfort & Convenience\n` | list[str] / object | string or multi-hot | Konfor & kolaylık donanımları listesi. |
| `\nEntertainment & Media\n` | list[str] / object | string or multi-hot | Multimedya/infotainment donanımları listesi. |
| `\nSafety & Security\n` | list[str] / object | string or multi-hot | Güvenlik donanımları listesi. |
| `\nExtras\n` | list[str] / object | string or multi-hot | Ekstra donanımlar listesi. |

**Modelleme notu (kısa):** Bu alanlar EDA’da “join text” ile okunur; modelde genelde `equipment_count` veya `has_feature_X` gibi 0/1 flag’lere çevrilir.

---

## 📝 J) Free Text (Serbest metin)
| Column | Raw format/type | Target type | Description |
|---|---|---|---|
| `desc` | long text | dropped or NLP | Uzun ilan açıklaması. İlk fazda genelde drop edilir (çok gürültülü). |
