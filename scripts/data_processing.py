import re
from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_extract, col, udf, to_date
from pyspark.sql.types import IntegerType, FloatType

# Initialize Spark Session
spark = SparkSession.builder.appName("RetailSalesAnalysis").getOrCreate()

# Read Data from S3
raw_data_path = "s3://your-bucket/retail_data/raw/*.csv"
retail_df = spark.read.csv(raw_data_path, header=True, inferSchema=True)

# Handle Missing Values
retail_df = retail_df.dropna(subset=['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country'])

# Convert Data Types
retail_df = retail_df.withColumn('Quantity', col('Quantity').cast(IntegerType()))
retail_df = retail_df.withColumn('UnitPrice', col('UnitPrice').cast(FloatType()))
retail_df = retail_df.withColumn('InvoiceDate', to_date(col('InvoiceDate'), 'MM/dd/yyyy HH:mm'))

# Create Total Price Column
retail_df = retail_df.withColumn('TotalPrice', col('Quantity') * col('UnitPrice'))

# Define a UDF for cleaning the Description

def clean_description(desc):
    cleaned_desc = re.sub('[^A-Za-z0-9 ]+', '', desc)
    return cleaned_desc.strip().upper()

clean_description_udf = udf(clean_description)
retail_df = retail_df.withColumn('CleanDescription', clean_description_udf(col('Description')))

# Save Processed Data
processed_data_path = "s3://your-bucket/retail_data/processed/"
retail_df.write.parquet(processed_data_path, mode='overwrite')
