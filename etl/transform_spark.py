from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, count

def create_spark_session():
    """Initializes a local PySpark Engine Session."""
    return SparkSession.builder \
        .appName("FintechETLPipeline") \
        .master("local[*]") \
        .getOrCreate()

def clean_and_transform(df):
    """
    1. Filters out invalid/failed transactions
    2. Groups transactions by Customer to aggregate total spend
    """
    # Filter valid completed transactions with positive amount
    valid_df = df.filter((col("status") == "COMPLETED") & (col("amount") > 0))
    
    # Aggregation (Star-schema analytical metric)
    aggregated_df = valid_df.groupBy("customer_id").agg(
        _sum("amount").alias("total_spent"),
        count("transaction_id").alias("transaction_count")
    )
    return aggregated_df

if __name__ == "__main__":
    spark = create_spark_session()
    
    # 1. Extract: Read raw JSON
    input_path = "data/raw_transactions.json"
    raw_df = spark.read.json(input_path)
    print("--- RAW DATA INGESTED ---")
    raw_df.show()
    
    # 2. Transform: Clean and aggregate
    transformed_df = clean_and_transform(raw_df)
    print("--- TRANSFORMED ANALYTICS DATA ---")
    transformed_df.show()
    
    # 3. Load: Save as Parquet columnar format
    output_path = "data/output_parquet"
    transformed_df.write.mode("overwrite").parquet(output_path)
    print(f"--- SUCCESS: Data written to Parquet lake at {output_path} ---")
    
    spark.stop()