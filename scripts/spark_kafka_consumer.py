from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

spark = SparkSession.builder \
    .appName("KafkaTicketConsumer") \
    .master("local[*]") \
    .config(
        "spark.jars.packages",
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0"
    ) \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

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
    StructField("ticket_type", StringType())
])

raw_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "ticket_purchases_raw") \
    .option("startingOffsets", "latest") \
    .load()

parsed = raw_stream.select(
    from_json(col("value").cast("string"), schema).alias("data"),
    col("timestamp").alias("kafka_timestamp")
)

events = parsed.select("data.*", "kafka_timestamp") \
    .withColumn("purchase_timestamp", to_timestamp("purchase_timestamp")) \
    .withColumn(
        "ingest_timestamp",
        col("purchase_timestamp") +
        expr("""
            CASE
                WHEN rand() < 0.04 THEN INTERVAL 2 DAYS
                WHEN rand() < 0.15 THEN INTERVAL 1 DAY
                WHEN rand() < 0.30 THEN INTERVAL 6 HOURS
                ELSE INTERVAL 15 MINUTES
            END
        """)
    )
def process_batch(batch_df, batch_id):
    if batch_df.isEmpty():
        return

    # Simulate duplicate delivery (5% of events)
    dup_df = batch_df.sample(0.05, seed=42) \
        .withColumn(
            "ingest_timestamp",
            col("ingest_timestamp") +
            expr("""
                CASE
                    WHEN rand() < 0.01 THEN INTERVAL 2 DAYS
                    WHEN rand() < 0.10 THEN INTERVAL 6 HOURS
                    ELSE INTERVAL 15 MINUTES
                END
            """)
        )

    final_df = batch_df.unionByName(dup_df)

    final_df.write \
        .mode("append") \
        .parquet("../data/streaming_output")


query = events.writeStream \
    .foreachBatch(process_batch) \
    .option("checkpointLocation", "../data/streaming_output/checkpoint") \
    .trigger(processingTime="5 seconds") \
    .start()

query.awaitTermination()
