# API
api_url = 'https://api.livecoinwatch.com/exchanges/list'
token = '865087d8-64cb-409c-81e8-4341b5bd7c6f'
header = {
    'x-api-key': token
}
data = {
    "currency":"USD",
    "sort":"visitors",
    "order":"descending",
    "offset":0,
    "limit":10,
    "meta": "true"
}


# Kafka
kafka_broker = 'dbaas.abriment.com:32744'
kafka_topic = 'data'

# DB
db_host = 'dbaas.abriment.com'
db_port = '31811'
db_database = 'process'
db_conn = f'jdbc:postgresql://{db_host}:{db_port}/{db_database}'
db_username = 'postgres'
db_password = '7rS86n2Z'
db_table = 'aggregates'

# Spark
checkpoint_location = '/tmp/spark-local-dir-1'