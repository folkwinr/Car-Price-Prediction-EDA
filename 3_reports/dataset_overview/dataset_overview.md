# Dataset Overview — AutoScout24 Car Listings (Raw)

## 1) Purpose (Why this dataset exists)
This dataset contains **raw car listings** collected from AutoScout24.  
The main goals are:
- understand which factors affect **car price**
- prepare the data for **analysis and modeling**
- build a clean dataset for the next project steps:
  - **Part 01:** Data Cleaning  
  - **Part 02:** Filling Missing Values  
  - **Part 03:** Outlier Handling  

---

## 2) Size and General Structure
- **Rows:** ~29,480 listings  
- **Columns:** **58** raw columns  
- **Format:** JSON → pandas DataFrame  

In the raw data, many columns look like `object` in pandas because:
- some numbers are stored as **text** (example: `"12,900 €"`, `"145,000 km"`)
- some columns contain **lists** (equipment features)
- some date fields are saved as **strings**

So the raw dataset is not fully ready for direct analysis.

---

## 3) What information is inside? (Main data blocks)
You can see the dataset in these main blocks:

1) **Listing Identity & Seller**
- brand/model fields, seller type, location, offer number  
- useful for grouping and segmentation

2) **Price & Usage**
- price and mileage  
- these are core variables for analysis

3) **Dates & Availability**
- first registration, production date, availability info  
- used to create **age**, but some fields are often missing

4) **Body & Interior/Exterior**
- body type, doors, seats, and also color/upholstery fields  
- good for segmentation, but color/upholstery can have many missing values

---

## 4) Missing Values (General view)
Missing values are normal in listing data because sellers do not fill every field.

Typical patterns:
- WLTP-related fields often have **very high missing values**
- EV-only fields (battery, range) are missing for most non-EV cars
- service and inspection fields can be missing a lot

This is why the project needs:
- cleaning rules (Part 01),
- smart filling methods (Part 02),
- careful outlier checks (Part 03).

---

## 5) Final Summary (Simple conclusion)
This raw dataset is **messy but valuable**.  
It includes strong signals for price analysis (price, mileage, dates, body info), but it needs work because:
- many values are not in the correct type,
- some columns are lists,
- many columns have missing values.

After proper cleaning and preparation, it becomes a strong base for deeper analysis and modeling.
