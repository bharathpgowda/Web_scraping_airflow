from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.python import PythonOperator
import googleapiclient.discovery
from googleapiclient.errors import HttpError
import pandas as pd
import s3fs

def run_youtube_etl():
  DEVELOPER_KEY = " "
  VIDEO_ID = "CFDCurqOERU"
  youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=DEVELOPER_KEY)

  try:
    response = youtube.commentThreads().list(
      part="snippet",
      videoId=VIDEO_ID,
      textFormat="plainText",
      maxResults=100
    ).execute()

    comments = []
    for item in response["items"]:
      comment_text= item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
      publish_time = item['snippet']['topLevelComment']['snippet']['publishedAt']
      likes = item["snippet"]["topLevelComment"]["snippet"]["likeCount"]
      comments.append({"comment": comment_text, "num_of_likes": likes,"publish_time":publish_time})
    df = pd.DataFrame(comments)
    df.to_csv("s3://endtoendairflow-bucket/youtube_comments.csv")


  except HttpError as error:
    print(f"An Http error {error.http_status} occurred:\n {error.content}")
    return None    


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 9, 21),
    'email': ['bharath19rocks@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=15)
}


dag = DAG(
  'youtube_new_dag_1',
  default_args=default_args,
  description='My first etl code'
)

run_etl = PythonOperator(
  task_id='complete_etl',
  python_callable=run_youtube_etl,
  dag=dag,
)
run_etl
