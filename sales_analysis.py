import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# 1. Load the dataset
# Encoding='unicode_escape' handles special characters often found in Kaggle sales files
df = pd.read_csv("sales_data_sample.csv", encoding="unicode_escape")

print("--- Data Columns Found ---")
print(df.columns.tolist())

# 2. Standardize Column Names (Mapping Kaggle standard names to variables)
# Kaggle datasets usually use uppercase 'SALES', 'ORDERDATE', and 'PRODUCTLINE'
sales_col = "SALES" if "SALES" in df.columns else "Sales"
date_col = "ORDERDATE" if "ORDERDATE" in df.columns else "Order_Date"
product_col = "PRODUCTLINE" if "PRODUCTLINE" in df.columns else "Product"

# 3. Data Cleaning & Date Parsing
df[date_col] = pd.to_datetime(df[date_col])
df["Year"] = df[date_col].dt.year
df["Month"] = df[date_col].dt.strftime("%B")
df["Month_Num"] = df[date_col].dt.month

# 4. Analysis: Product Performance
product_performance = (
    df.groupby(product_col)[sales_col].sum().sort_values(ascending=False)
)

# 5. Analysis: Monthly/Seasonal Trends (Sorted chronologically by Month_Num)
monthly_trends = (
    df.groupby(["Month_Num", "Month"])[sales_col].sum().reset_index()
)

# --- VISUALIZATIONS ---
sns.set_theme(style="whitegrid")
plt.figure(figsize=(15, 6))

# Chart 1: Product Performance Bar Chart
plt.subplot(1, 2, 1)
sns.barplot(
    x=product_performance.values, y=product_performance.index, palette="rocket"
)
plt.title("Total Revenue by Product Line")
plt.xlabel("Sales Revenue ($)")
plt.ylabel("Product Category")

# Chart 2: Seasonal/Monthly Line Chart
plt.subplot(1, 2, 2)
sns.lineplot(
    data=monthly_trends,
    x="Month",
    y=sales_col,
    marker="o",
    color="crimson",
    linewidth=2.5,
)
plt.xticks(rotation=45)
plt.title("Monthly Sales Trends (Seasonal Analysis)")
plt.xlabel("Month")
plt.ylabel("Total Sales Revenue ($)")

plt.tight_layout()

# Save outputs cleanly for your GitHub repo showcase
os.makedirs("output", exist_ok=True)
plt.savefig("output/sales_analysis_plots.png")
print("\nSuccess! Analysis plots saved to 'output/sales_analysis_plots.png'")

# Display the charts on your screen
plt.show()