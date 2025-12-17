# 📘 Data Dictionary — Raw Dataset Columns (AutoScout24)

> **Source:** `as24_cars.json` (raw listings)  
> **Total columns:** 58  
> **Note:** In pandas, many raw columns may appear as `object`. Here, **Raw format/type** describes how values usually look in the raw data.

---

## 🧾 A) Listing Identity & Seller
| Column | Raw format/type | Target type | Description |
|---|---|---|---|
| `make_model` | string | string/category | Combined brand + model name (very strong for segmentation). |
| `short_description` | string | string | Short listing title / summary text. |
| `make` | string | string/category | Brand (manufacturer). |
| `model` | string | string/category | Model name. |
| `location` | string | string/category | Seller/listing location (city/region). |
| `Offer number` | string / ID-like | string | Offer/listing identifier. Usually not used in modeling (leakage risk). |
| `seller` | string/category | category | Seller type (dealer/private, etc.). |
| `Country version` | string/category | category | Country specification/version of the car (often missing). |
| `Model code` | string / ID-like | string | Manufacturer/model code (often missing). |
| `desc` | long free text | dropped or NLP | Long description text (often dropped in early phases). |

---

## 💰 B) Price & Usage
| Column | Raw format/type | Target type | Description |
|---|---|---|---|
| `price` | numeric-like string (currency/separators possible) | numeric (float/int) | Listing price; parsed into a numeric value. |
| `Mileage` | numeric-like string (km + separators possible) | numeric (int) | Mileage; cleaned and converted to numeric (usually km). |

---

## 🗓️ C) Dates & Availability
| Column | Raw format/type | Target type | Description |
|---|---|---|---|
| `First registration` | date/year-like string | int (year) / derived `age` | First registration year/date; often used to create `age`. |
| `Production date` | date/year-like string | int/year or dropped | Production date (often very missing). |
| `Available from` | date-like string | date/string | From which date the car is available (often missing). |
| `Availability` | string/category | category | Availability status (often missing). |

---

## 🚗 D) Body & Interior/Exterior
| Column | Raw format/type | Target type | Description |
|---|---|---|---|
| `Body type` | string/category | category | Body type (SUV, Sedan, Hatchback, etc.). |
| `Type` | string/category | category | Variant/type information from the listing (can vary by seller). |
| `Doors` | numeric-like string | int | Number of doors. |
| `Seats` | numeric-like string | int | Number of seats. |
| `Colour` | string/category | category | General exterior color. |
| `Paint` | string/category | category | Paint type (metallic/solid, etc.). |
| `Manufacturer colour` | string | string/category | OEM/manufacturer color name. |
| `Upholstery` | string/category | category | Upholstery material/type (cloth/leather, etc.). |
| `Upholstery colour` | string/category | category | Upholstery color. |

---

## ⚙️ E) Powertrain & Technical Specs
| Column | Raw format/type | Target type | Description |
|---|---|---|---|
| `Power` | string (often includes kW & hp) / sometimes list | numeric split: `power_kW`, `power_hp` | Power information; usually split into kW and hp numeric columns. |
| `Engine size` | numeric-like string | numeric | Engine displacement (raw format can vary; parsed to numeric). |
| `Cylinders` | numeric-like string | int | Number of cylinders. |
| `Gearbox` | string/category | category | Gearbox type (Manual/Automatic). |
| `Gears` | numeric-like string | int | Number of gears. |
| `Drivetrain` | string/category | category | Drivetrain (FWD/RWD/AWD). |
| `Empty weight` | numeric-like string | numeric | Empty weight (often kg). |

---

## ⛽ F) Fuel, Consumption & EV Fields
| Column | Raw format/type | Target type | Description |
|---|---|---|---|
| `Fuel type` | string/category | category | Main fuel type (Petrol/Diesel/Electric/Hybrid, etc.). |
| `Other fuel types` | string/category | category | Additional fuel types (often missing). |
| `Fuel consumption` | mixed string / sometimes nested | numeric features (`cons_avg`, `cons_city`, `cons_country`) | Consumption field; often split into clear numeric parts. |
| `Fuel consumption (WLTP)` | numeric-like string | numeric | WLTP fuel consumption (often missing). |
| `Power consumption` | numeric-like string | numeric | Electric power consumption (EV/Hybrid; often missing). |
| `Power consumption (WLTP)` | numeric-like string | numeric | WLTP electric consumption (very missing). |
| `Electric Range (WLTP)` | numeric-like string | numeric | WLTP electric range (very missing). |
| `Battery Ownership` | string/category | category | Battery ownership (owned/leased; usually missing). |

---

## 🌿 G) Emissions & Efficiency
| Column | Raw format/type | Target type | Description |
|---|---|---|---|
| `CO₂-emissions` | numeric-like string | numeric | CO₂ emissions (often g/km). |
| `CO₂-emissions (WLTP)` | numeric-like string | numeric | WLTP CO₂ emissions (often missing). |
| `CO₂-efficiency` | string/category | category | CO₂ efficiency label/class (format may vary). |
| `Energy efficiency class` | string/category | category | Energy efficiency class (A/B/C...). |
| `Emission class` | string/category | category | Emission standard (Euro 5/6, etc.). |
| `Emissions sticker` | string/category | category | Emissions/environment sticker label (country-specific). |

---

## 🧰 H) Service, Inspection & History
| Column | Raw format/type | Target type | Description |
|---|---|---|---|
| `Warranty` | string/category | category/bool | Warranty info (yes/no/period). |
| `Full service history` | string/category | bool/category | Full service history availability. |
| `Last service` | date-like string | date/string | Last service date (often missing). |
| `General inspection` | date-like / string | date/string/category | General inspection info (often missing). |
| `Previous owner` | numeric-like string | int | Number of previous owners (parsed to numeric when possible). |
| `Non-smoker vehicle` | bool-like string | bool/category | Non-smoker vehicle flag. |
| `Last timing belt change` | date-like / string | date/string | Timing belt change info (often missing). |
| `Taxi or rental car` | bool-like string | bool/category | Taxi/rental history flag (often missing). |

---

## 🧩 I) Equipment Groups (List fields)
> These 4 raw column names include leading/trailing `\n` characters.

| Column | Raw format/type | Target type | Description |
|---|---|---|---|
| `\nComfort & Convenience\n` | list[str] / object | string or multi-hot | Comfort & convenience equipment list. |
| `\nEntertainment & Media\n` | list[str] / object | string or multi-hot | Entertainment/infotainment equipment list. |
| `\nSafety & Security\n` | list[str] / object | string or multi-hot | Safety & security equipment list. |
| `\nExtras\n` | list[str] / object | string or multi-hot | Extras equipment list. |

**Modeling note (short):** For EDA, joining list items into text is readable. For modeling, these are usually better as counts or 0/1 flags (multi-hot).

---
