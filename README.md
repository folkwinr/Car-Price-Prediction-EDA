<div style="
    background: radial-gradient(circle at top left, #0f172a 0%, #020617 40%, #22d3ee 120%);
    border-radius: 22px;
    padding: 26px 30px 30px 30px;
    border: 2px solid #38bdf8;
    box-shadow:
        0 0 10px rgba(56, 189, 248, 0.9),
        0 0 30px rgba(59, 130, 246, 0.8),
        0 0 80px rgba(37, 99, 235, 0.7);
    margin: 18px 0 30px 0;
    text-align: center;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif;
">

  <div style="
      font-size: 12px;
      letter-spacing: 0.4em;
      text-transform: uppercase;
      color: #bae6fd;
      margin-bottom: 8px;
  ">
    MACHINE LEARNING PROJECT
  </div>

  <div style="
      font-size: 34px;
      font-weight: 900;
      color: #e0f2fe;
      text-shadow:
          0 0 8px #38bdf8,
          0 0 20px #0ea5e9,
          0 0 40px #3b82f6;
      margin-bottom: 6px;
  ">
    🚗 CAR PRICE PREDICTION – END-TO-END PIPELINE
  </div>

  <div style="
      font-size: 13px;
      color: #e5e7eb;
      max-width: 720px;
      margin: 0 auto;
  ">
    Gerçek ilan verileriyle, ham ve dağınık bir veri setinden başlayıp
    <b>temizleme → feature engineering → modelleme → değerlendirme</b>
    adımlarının hepsini kapsayan uçtan uca bir fiyat tahmin projesi.
  </div>
</div>


<!-- ======================= QUICK INFO STRIP ======================= -->

<div style="
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 24px;
  font-family: system-ui, sans-serif;
">

  <div style="
      flex: 1 1 160px;
      background: linear-gradient(135deg, rgba(56,189,248,0.15), rgba(15,23,42,0.95));
      border-radius: 14px;
      padding: 10px 14px;
      border: 1px solid rgba(56,189,248,0.5);
      color: #e5e7eb;
      font-size: 12px;
      box-shadow: 0 0 12px rgba(15,23,42,0.9);
  ">
    <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.15em; color:#93c5fd;">
      🎯 Goal
    </div>
    <div style="margin-top: 4px;">
      İlan özelliklerine bakarak <b>araba satış fiyatını</b> mümkün olduğunca
      doğru tahmin etmek.
    </div>
  </div>

  <div style="
      flex: 1 1 160px;
      background: linear-gradient(135deg, rgba(129,140,248,0.2), rgba(15,23,42,0.95));
      border-radius: 14px;
      padding: 10px 14px;
      border: 1px solid rgba(129,140,248,0.6);
      color: #e5e7eb;
      font-size: 12px;
      box-shadow: 0 0 12px rgba(15,23,42,0.9);
  ">
    <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.15em; color:#a5b4fc;">
      📦 Dataset
    </div>
    <div style="margin-top: 4px;">
      Gerçek araç ilanları · <b>marka/model, motor, kapı sayısı, yakıt, km,
      ülke versiyonu, kayıt yılı</b> ve daha fazlası.
    </div>
  </div>

  <div style="
      flex: 1 1 160px;
      background: linear-gradient(135deg, rgba(52,211,153,0.18), rgba(15,23,42,0.95));
      border-radius: 14px;
      padding: 10px 14px;
      border: 1px solid rgba(52,211,153,0.65);
      color: #e5e7eb;
      font-size: 12px;
      box-shadow: 0 0 12px rgba(15,23,42,0.9);
  ">
    <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.15em; color:#6ee7b7;">
      🧠 Models
    </div>
    <div style="margin-top: 4px;">
      <b>Linear Regression, Random Forest, Gradient Boosting</b> gibi
      regresyon algoritmalarıyla karşılaştırmalı deneyler.
    </div>
  </div>

</div>


---

### 📚 Project Overview (Projenin Özeti)

Bu proje, gerçek dünyadaki <b>dağınık ve kirli bir araç ilan veri setini</b> alıp,
aşağıdaki adımlarla üretim-benzeri bir <b>Car Price Prediction</b> pipeline’ına dönüştürmeyi hedefler:

- 🔍 **Exploratory Data Analysis (EDA)** – veri dağılımı, aykırı değerler, eksik değerler  
- 🧹 **Data Cleaning** – boş / anlamsız satırlar, hatalı formatlar, tutarsız etiketler  
- 🧬 **Feature Engineering** – yeni değişkenler üretme, nadir kategorileri gruplayıp sadeleştirme  
- 🤖 **Model Training & Tuning** – farklı algoritmalarla fiyat tahmini, karşılaştırma ve optimizasyon  
- 📈 **Evaluation & Interpretation** – hata metrikleri, feature importance, modelin mantığını okumak  

---

<div style="
  background: radial-gradient(circle at top left, rgba(56,189,248,0.18), rgba(15,23,42,0.98));
  border-radius: 18px;
  padding: 18px 20px 16px 20px;
  border: 1px solid rgba(56,189,248,0.7);
  margin: 18px 0;
  box-shadow:
    0 0 14px rgba(56,189,248,0.7),
    0 0 30px rgba(15,23,42,0.95);
  font-family: system-ui, sans-serif;
">

  <div style="font-size: 14px; font-weight: 700; color:#e0f2fe; margin-bottom:8px;">
    🧹 1. Data Cleaning Highlights (Veri Temizleme Özeti)
  </div>

  <ul style="margin: 0; padding-left: 18px; color:#e5e7eb; font-size: 13px;">
    <li><b>Completely empty rows</b> (tüm kolonları NaN olan kayıtlar) tespit edilip dataset’ten çıkarıldı.</li>
    <li><code>price</code> sütunundaki karmaşık format (&quot;€ 16,950.-&quot; gibi) regex ile temizlendi ve sayıya çevrildi.</li>
    <li><code>short_description</code> gibi aşırı yüksek kardinaliteli, modelleme için sinyal taşımayan
        serbest metin kolonları kaldırıldı.</li>
    <li><code>country_version</code> ve benzeri list-formatlı kolonlar, tekil etikete indirgenip
        gereksiz boşluk ve karakterlerden arındırıldı.</li>
    <li><code>doors</code> gibi numerik olması gereken özellikler önce metinden temizlenip sonra
        <b>numeric</b> tipe cast edildi.</li>
  </ul>
</div>


<div style="
  background: radial-gradient(circle at top right, rgba(129,140,248,0.35), rgba(15,23,42,0.98));
  border-radius: 18px;
  padding: 18px 20px 16px 20px;
  border: 1px solid rgba(129,140,248,0.7);
  margin: 18px 0;
  box-shadow:
    0 0 14px rgba(129,140,248,0.7),
    0 0 30px rgba(15,23,42,0.95);
  font-family: system-ui, sans-serif;
">

  <div style="font-size: 14px; font-weight: 700; color:#e0f2fe; margin-bottom:8px;">
    🧬 2. Feature Engineering (Özellik Tasarımı)
  </div>

  <ul style="margin: 0; padding-left: 18px; color:#e5e7eb; font-size: 13px;">
    <li>Yaş hesaplama: <code>car_age = listing_year - registration_year</code></li>
    <li>Kategorik değişkenler için <b>one-hot encoding / target encoding</b> stratejileri.</li>
    <li>Nadir marka / model kombinasyonlarını gruplayarak <b>high cardinality</b> problemini azaltma.</li>
    <li>Güçlü korelasyon gösteren sayısal değişkenlerden (km, power, engine size vb.)
        model için daha anlamlı türetilmiş feature’lar oluşturma.</li>
  </ul>
</div>


<div style="
  background: radial-gradient(circle at top left, rgba(52,211,153,0.28), rgba(15,23,42,0.98));
  border-radius: 18px;
  padding: 18px 20px 16px 20px;
  border: 1px solid rgba(45,212,191,0.8);
  margin: 18px 0;
  box-shadow:
    0 0 16px rgba(45,212,191,0.7),
    0 0 30px rgba(15,23,42,0.95);
  font-family: system-ui, sans-serif;
">

  <div style="font-size: 14px; font-weight: 700; color:#ecfeff; margin-bottom:8px;">
    🤖 3. Modeling & Evaluation (Modelleme ve Değerlendirme)
  </div>

  <ul style="margin: 0; padding-left: 18px; color:#e5e7eb; font-size: 13px;">
    <li>Baseline olarak <b>Linear Regression</b> ile başlangıç performansı ölçüldü.</li>
    <li>Daha sonra <b>Random Forest Regressor</b>, <b>Gradient Boosting</b> ve benzeri ağaç tabanlı
        yöntemlerle performans karşılaştırması yapıldı.</li>
    <li>Değerlendirme metrikleri: <b>MAE, RMSE, R²</b> – hem train hem validation set üzerinde.</li>
    <li>Feature importance analizleri ile modelin <b>fiyatı en çok hangi özelliklere göre belirlediği</b> görselleştirildi.</li>
  </ul>
</div>


### 🛠️ Tech Stack

- 🐍 **Python** – ana dil  
- 📊 **pandas, NumPy** – veri işleme ve temizleme  
- 📈 **Matplotlib / Seaborn** – EDA, görselleştirme  
- 🤖 **scikit-learn** – modelleme, cross-validation, tuning  
- 🔁 **Jupyter Notebook** – deneysel çalışma ortamı  

---

### ▶️ How to Run (Nasıl Çalıştırılır?)

```bash
# 1. Ortamı oluştur
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Gerekli paketleri kur
pip install -r requirements.txt

# 3. Notebook'u başlat
jupyter notebook
# veya
jupyter lab

