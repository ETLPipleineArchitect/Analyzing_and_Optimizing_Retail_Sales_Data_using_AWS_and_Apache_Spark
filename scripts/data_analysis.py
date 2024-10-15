from pyspark.sql import SparkSession

# Initialize Spark Session
spark = SparkSession.builder.appName("RetailSalesAnalysis").getOrCreate()

# Load Processed Data
processed_data_path = "s3://your-bucket/retail_data/processed/"
retail_df = spark.read.parquet(processed_data_path)

retail_df.createOrReplaceTempView("retail_data")

# Top 10 Products by Sales
top_products = spark.sql("""
  SELECT CleanDescription, SUM(Quantity) as TotalQuantity
  FROM retail_data
  GROUP BY CleanDescription
  ORDER BY TotalQuantity DESC
  LIMIT 10
""")
top_products.show()

top_products.write.csv("s3://your-bucket/retail_data/output/top_products.csv", mode='overwrite')

# Monthly Sales Trend
monthly_sales = spark.sql("""
  SELECT DATE_FORMAT(InvoiceDate, 'yyyy-MM') as Month, SUM(TotalPrice) as TotalSales
  FROM retail_data
  GROUP BY Month
  ORDER BY Month
""")
monthly_sales.show()

monthly_sales.write.csv("s3://your-bucket/retail_data/output/monthly_sales.csv", mode='overwrite')

# Top Customers by Revenue
top_customers = spark.sql("""
  SELECT CustomerID, SUM(TotalPrice) as TotalSpent
  FROM retail_data
  GROUP BY CustomerID
  ORDER BY TotalSpent DESC
  LIMIT 10
""")
top_customers.show()

top_customers.write.csv("s3://your-bucket/retail_data/output/top_customers.csv", mode='overwrite')
