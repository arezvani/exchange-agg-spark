# exchange-agg-spark
Structure Streaming with Kafka, Spark, Postgresql and Grafana (Exchange(coins) aggregation)

## Generate data
we write a Python script that generates data in 2 way:

1- `random`: Weather data for a city and publishes it to the Kafka topic. We’re simulating the weather data for simplicity.

2- `exchanges`: Call [livecoinwatch](https://www.livecoinwatch.com/tools/api) and get top 10 of coins.

> *Note:*
> In exchanges api, we also add time to each record.

## Write data to kafka
Then we write data to kafka after converting that to json and utf-8 encoding.

After starting your script, it will continuously send data every second (can be customized) to your Kafka topic. You can consume this data from the topic in another application or service that listens to the Kafka topic.

![image](https://github.com/arezvani/exchange-agg-spark/assets/20871524/01a8282e-269d-49c9-910c-9cc49228cc3e)

![image](https://github.com/arezvani/exchange-agg-spark/assets/20871524/a7903627-982f-4143-bb99-75439b6dbf19)

## Data Processing with PySpark
To process streaming data with PySpark and store it in PostgreSQL, you need to set up a structured streaming pipeline. This pipeline will read from the Kafka topic, parse and process the data, and then store the results in your PostgreSQL database.

We define the schema of the data. Then read from Kafka topic and Deserialize the JSON data from the Kafka topic and convert the timestamp to the appropriate data type. 

Then apply windowed aggregation over a 60-second window.

## Write to PostgreSQL

Create table in PostgreSQL:

```sql
CREATE TABLE public.aggregates (
	window_start timestamp NULL,
	window_end timestamp NULL,
	code varchar NULL,
	avg_vol float4 NULL
);
```

Extract window start and end times, along with the aggregated data, before writing to the database. Finally, write the output data into your PostgreSQL database.

With this setup, your PySpark application reads streaming data from a Kafka topic, processes it in 60-second windows, and writes the aggregated results to a PostgreSQL database. This method allows for near-real-time analytics, which is crucial for timely insights and decision-making.

We run our code with [Spark Operator](https://github.com/GoogleCloudPlatform/spark-on-k8s-operator) and Spark application on k8s.


## Visualize data

We use Grafana and PostgreSQL datasource:

![image](https://github.com/arezvani/exchange-agg-spark/assets/20871524/4925df15-3555-4f22-9fbf-e4f04bfbfb8e)
