from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, to_timestamp, window, avg, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, TimestampType
import config

def main():
    spark = SparkSession.builder.appName("RealTimeProcessing").getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    # Schema

    # Weather
    # schema = StructType([
    #     StructField("city", StringType(), True),
    #     StructField("temperature", DoubleType(), True),
    #     StructField("humidity", IntegerType(), True),
    #     StructField("timestamp", StringType(), True)  # or TimestampType()
    # ])

    # Exchange
    schema = StructType([
        StructField("code", StringType(), True),
        StructField("markets", IntegerType(), True),
        StructField("volume", IntegerType(), True),
        StructField("bidTotal", DoubleType(), True),
        StructField("askTotal", DoubleType(), True),
        StructField("depth", DoubleType(), True),
        StructField("visitors", IntegerType(), True),
        StructField("volumePerVisitor", IntegerType(), True),
    ])

    # Read from Kafka
    topic = config.kafka_topic

    df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", config.kafka_broker).option("subscribe", topic).option("startingOffsets", "latest").load()

    # Weather
    # data = df.selectExpr("CAST(value AS STRING)") \
    #     .select(from_json("value", schema).alias("data")) \
    #     .select("data.*") \
    #     .withColumn("timestamp", to_timestamp("timestamp", "yyyy-MM-dd HH:mm:ss"))
    
    # Exchange
    data = df.selectExpr("CAST(value AS STRING)") \
        .select(from_json("value", schema).alias("data")) \
        .select("data.*") \
        .withColumn("time", to_timestamp("time", "yyyy-MM-dd HH:mm:ss")) # timestamp

    # Window
    windowed_data = data \
        .groupBy(
            window(col("time"), "60 seconds"), # timestamp
            col("code") # city
        ) \
        .agg(avg(col("volume")).alias("avg_vol")) # temperature avg_temp 

    # Write
    output_data = windowed_data.select(
        col("window.start").alias("window_start"),
        col("window.end").alias("window_end"),
        col("code"),
        col("avg_vol") # avg_temp
    )

    # Write to PostgreSQL
    jdbc_url = config.db_conn  # using connection string
    jdbc_properties = {
        "user": config.db_username,
        "password": config.db_password,
        "driver": "org.postgresql.Driver"
    }

    checkpoint_location = config.checkpoint_location

    query = output_data.writeStream \
        .outputMode("update") \
        .foreachBatch(lambda batch_df, epoch_id: batch_df.write.jdbc(
            url=jdbc_url,
            table=config.db_table,
            mode="append",
            properties=jdbc_properties
        )) \
        .option("checkpointLocation", checkpoint_location) \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    main()