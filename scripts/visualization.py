import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data from S3 (Assuming data is downloaded locally)
monthly_sales = pd.read_csv('data/monthly_sales.csv')

tplt.figure(figsize=(12, 6))
sns.lineplot(data=monthly_sales, x='Month', y='TotalSales')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.show()

# Load Top Products
top_products = pd.read_csv('data/top_products.csv')
plt.figure(figsize=(12, 6))
sns.barplot(data=top_products, x='TotalQuantity', y='CleanDescription')
plt.title('Top 10 Products by Quantity Sold')
plt.xlabel('Total Quantity Sold')
plt.ylabel('Product')
plt.show()
