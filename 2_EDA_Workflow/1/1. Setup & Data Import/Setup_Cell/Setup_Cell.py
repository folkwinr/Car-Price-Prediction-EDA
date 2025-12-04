# ====================================================
# 🚀 AUTO SCOUT EDA PROJECT — SETUP CELL
# ====================================================


# ====================================================
# 1. CORE LIBRARIES
# ====================================================
import numpy as np
import pandas as pd


# ====================================================
# 2. VISUALIZATION LIBRARIES
# ====================================================
import matplotlib.pyplot as plt
import seaborn as sns


# ====================================================
# 3. DISPLAY TOOLS
# ====================================================
from IPython.display import display


# ====================================================
# 4. UTILITIES
# ====================================================
import re
import warnings


# ====================================================
# 5. WARNING SETTINGS
# ====================================================
warnings.filterwarnings("ignore")


# ====================================================
# 6. MATPLOTLIB & SEABORN SETTINGS
# ====================================================
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["figure.dpi"] = 100

sns.set_style("whitegrid")
pd.set_option("display.float_format", lambda x: "%.2f" % x)


# ====================================================
# 7. PANDAS DISPLAY SETTINGS
# ====================================================
pd.options.display.max_rows = 300
pd.options.display.max_columns = 100


# ====================================================
# 8. NOTEBOOK INLINE PLOTTING
# ====================================================
%matplotlib inline
