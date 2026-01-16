from pyspark.sql import SparkSession
from pyspark.sql import functions as F

#defining Spark session 
spark = SparkSession.builder \
    .appName("SmartLogiTrack_Clean") \
    .config("spark.jars.packages", "org.postgresql:postgresql:42.7.1") \
    .getOrCreate()

# readind data
df = spark.read.parquet("/opt/airflow/data/dataset.parquet")

# data cleaning(durationmins=dropoff - pickup in minutes)
df = df.withColumn("duration_minutes", 
    (F.unix_timestamp("tpep_dropoff_datetime") - F.unix_timestamp("tpep_pickup_datetime")) / 60
)
# filtering invalid data
df = df.filter(
    (F.col("duration_minutes") > 0) & 
    (F.col("trip_distance") > 0) & 
    (F.col("trip_distance") <= 200)
)

# feature Engineering
df = df.withColumn("pickuphour", F.hour("tpep_pickup_datetime")) \
       .withColumn("dayof_week", F.dayofweek("tpep_pickup_datetime")) \
       .withColumn("month", F.month("tpep_pickup_datetime"))

# saving to Postgres(taxi_silver table)
df.write.format("jdbc") \
    .option("url", "jdbc:postgresql://postgres:5432/taxi_db") \
    .option("driver", "org.postgresql.Driver") \
    .option("dbtable", "taxi_silver") \
    .option("user", "postgres") \
    .option("password", "12345678") \
    .mode("overwrite").save()

# Parquet for training script
df.write.mode("overwrite").parquet("/opt/airflow/data/silver_taxi_data")

# stopping spark session
spark.stop()