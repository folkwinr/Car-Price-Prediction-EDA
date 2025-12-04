# 🔍 check_obj_columns() Function  
*A simple utility to detect mixed data types inside object columns.*

---

## 📘 Overview  
The `check_obj_columns()` function checks all **object** columns in a Pandas DataFrame and reports:

- which columns have **mixed data types**  
- or prints **NO PROBLEM** if all object columns use a single consistent type  

Mixed types can cause issues during cleaning, encoding, or modeling.

---

## 🧠 How It Works

### 1️⃣ Select object columns  
The function looks only at columns with data type **object**.

### 2️⃣ Check each value’s data type  
Inside each column, every value is converted into its Python type  
(e.g., `str`, `int`, `float`, `NoneType`).

### 3️⃣ Detect mixed types  
If a column contains more than one unique type, it is marked as a problem.

### 4️⃣ Print results  
- If any columns have mixed types → print them in **red**  
- If none have problems → print **NO PROBLEM** in **green**

---

## 🧪 Example Usage

```python
from check_obj_columns import check_obj_columns

check_obj_columns(df)

Example output:

Column fuel_type has mixed object types.
Column model has mixed object types.

Or if everything is clean:

NO PROBLEM with the data types of Columns in the DataFrame.




