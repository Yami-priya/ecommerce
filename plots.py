import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set(style="whitegrid")

# Load CSV files
eligibility_df = pd.read_csv("eligibility.csv")
ad_sales_df = pd.read_csv("ad_sales.csv")
total_sales_df = pd.read_csv("total_sales.csv")

# Create output directory if not exists
output_dir = "visualizations"
os.makedirs(output_dir, exist_ok=True)

# 1. Eligibility Status Distribution
plt.figure(figsize=(6, 4))
eligibility_counts = eligibility_df['eligibility'].value_counts()
sns.barplot(x=eligibility_counts.index, y=eligibility_counts.values, palette="Set2")
plt.title("Eligibility Status Distribution")
plt.xlabel("Eligibility")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(f"{output_dir}/eligibility_status_distribution.png")
plt.close()

# 2. Top 10 Products by Ad Sales
plt.figure(figsize=(8, 5))
top_ad_sales = ad_sales_df.groupby('item_id')['ad_sales'].sum().nlargest(10)
top_ad_sales.plot(kind='bar', color='skyblue')
plt.title("Top 10 Products by Ad Sales")
plt.xlabel("Item ID")
plt.ylabel("Ad Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{output_dir}/top_10_ad_sales.png")
plt.close()

# 3. Total Sales by Product Category (if exists)
if 'product_category' in total_sales_df.columns:
    plt.figure(figsize=(10, 5))
    category_sales = total_sales_df.groupby('product_category')['total_sales'].sum().sort_values(ascending=False)
    category_sales.plot(kind='bar', color='orange')
    plt.title("Total Sales by Product Category")
    plt.xlabel("Product Category")
    plt.ylabel("Total Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/total_sales_by_category.png")
    plt.close()

# 4. Correlation Heatmap of Total Sales Metrics
plt.figure(figsize=(8, 6))
correlation = total_sales_df.select_dtypes(include='number').corr()
sns.heatmap(correlation, annot=True, cmap="coolwarm", fmt=".2f", square=True)
plt.title("Correlation Heatmap of Total Sales Metrics")
plt.tight_layout()
plt.savefig(f"{output_dir}/sales_correlation_heatmap.png")
plt.close()

print(f"✅ Visualizations saved in: {output_dir}/")
