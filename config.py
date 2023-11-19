# API
api_url = 'https://api.livecoinwatch.com/exchanges/list'
token = '******-****-****-****-*******'
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
kafka_broker = '**********:****'
kafka_topic = '***'

# DB
db_host = '**************'
db_port = '********'
db_database = '*******'
db_conn = f'jdbc:postgresql://{db_host}:{db_port}/{db_database}'
db_username = '*******'
db_password = '*********'
db_table = '*********'

# Spark
checkpoint_location = '/tmp/spark-local-dir-1'
