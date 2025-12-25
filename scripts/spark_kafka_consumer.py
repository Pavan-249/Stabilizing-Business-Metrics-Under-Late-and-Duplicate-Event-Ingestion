from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

spark = SparkSession.builder \
    .appName("KafkaTicketConsumer") \
    .master("local[*]") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0") \
    .getOrCreate()
schema = StructType([
    StructField("ticket_id", StringType()),
    StructField("match_id", StringType()),
    StructField("user_id", StringType()),
    StructField("user_email", StringType()),
    StructField("user_name", StringType()),
    StructField("stadium", StringType()),
    StructField("quantity", IntegerType()),
    StructField("price", DoubleType()),
    StructField("purchase_timestamp", StringType()),
    StructField("ticket_type", StringType()),
    # Add any other columns you have
])

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "ticket_purchases_raw").option("startingOffsets", "earliest") \
    .load()
parsed = df.select(
    from_json(col("value").cast("string"), schema).alias("data"),
    col("timestamp").alias("kafka_timestamp")  # When Kafka received it
)

# Flatten the JSON structure
events = parsed.select("data.*", "kafka_timestamp")

# Add ingest_timestamp (when Spark processes it)
events = events.withColumn("ingest_timestamp", current_timestamp())

# Convert purchase_timestamp string to actual timestamp
events = events.withColumn(
    "purchase_timestamp",
    to_timestamp(col("purchase_timestamp"))
)

# Calculate ingestion lag
events = events.withColumn(
    "ingestion_lag_seconds",
    unix_timestamp("ingest_timestamp") - unix_timestamp("purchase_timestamp")
)

# Write to console first (for testing)
query = events.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "data/streaming_output") \
    .option("checkpointLocation", "data/checkpoint") \
    .trigger(processingTime='5 seconds').start()

query.awaitTermination()
