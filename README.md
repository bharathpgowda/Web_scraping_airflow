End to end datapipeline to perform ETL process on youtube comments using GOOGLE API, Python and Apache Airflow.

Import "googleapiclient.discovery" to communicate and extract comments from youtube. "Airflow" is used as a workflow management tool. Code execution is done in an ubuntu server hosted in the "Amazon EC2 instance".Along with EC2 , two S3 buckets and one Lambda function is used.

Code is executed using "DAG" function in airflow.
