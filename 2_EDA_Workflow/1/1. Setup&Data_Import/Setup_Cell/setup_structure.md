# ⚙️ Setup Cell – Folder & File Explanation

This folder explains the **setup cell** used in the AutoScout EDA project.  
It includes all libraries and settings needed for a clean and easy workflow.

---

## 📁 libraries/  
This folder contains all import groups.

### 📌 core_libraries.py  
Basic Python tools:  
- `numpy` → numbers  
- `pandas` → data tables  

### 🎨 visualization_libraries.py  
Used for charts and plots:  
- `matplotlib`  
- `seaborn`  

### 👁️ display_tools.py  
Tools for showing data in Jupyter Notebook:  
- `display()`  

### 🧰 utilities.py  
Helper tools:  
- `re` → text cleaning  
- `warnings` → warning control  

---

## 📁 settings/  
This folder contains all notebook settings.

### 🚫 warning_settings.py  
- Turns off yellow warnings.  
- Makes the notebook cleaner and easier to read.

### 🎨 matplotlib_settings.py  
- Sets figure size.  
- Sets DPI.  
- Sets seaborn style.  
- Makes charts clean and good-looking.

### 📊 pandas_display_settings.py  
- Shows more rows and columns.  
- Formats numbers with 2 decimals.  
- Makes DataFrames easy to read.

### 🖼️ plotting_mode.py  
- Enables `%matplotlib inline`.  
- Shows plots directly inside the notebook.

---

## 📄 setup_cell.ipynb  
This is the final notebook cell that combines everything.  
It contains all imports and all settings in one clean block.
