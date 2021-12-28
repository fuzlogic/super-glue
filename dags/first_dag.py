import asyncio
import datetime as dt
import json
import os
import requests
from jsonpath_ng import parse

from airflow.models import DAG
from airflow.operators.python import PythonOperator
import databases

args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2021, 11, 15),
    'retries': 100,
    'retry_delay': dt.timedelta(minutes=1),
    'depends_on_past': False,
}

POSTS_URL = 'http://jsonplaceholder.typicode.com/posts'
FILENAME_RAW = os.path.abspath(os.path.join('result', 'posts_raw.json'))
FILENAME_PRC = os.path.abspath(os.path.join('result', 'posts_postprocessing.json'))
DATABASE_URL = f"postgresql://etl:Jyp2DRAEyugVRA5N@localhost:5432/etl_data"


def download_posts_dataset():
    response = requests.get(POSTS_URL, stream=True)
    response.raise_for_status()
    with open(FILENAME_RAW, 'w', encoding='utf-8') as f:
        for chunk in response.iter_lines():
            f.write(chunk.decode('utf-8'))


def transform_dataset():
    result = []
    with open(FILENAME_RAW, "r") as f:
        data = f.readlines()
        json_data = json.loads(''.join(data))
        for match in parse('[*].body').find(json_data):
            if match.context.value['userId'] == 1:
                result.extend(match.value.split('\n'))
    with open(FILENAME_PRC, 'w', encoding='utf-8') as f:
        f.write('\n'.join(result))


def save_dataset():
    async def do():
        database = databases.Database(DATABASE_URL)
        await database.connect()
        with open(FILENAME_PRC, "r") as f:
            data = f.readlines()
            for item in list(data):
                await database.execute('insert into log (data) values (:data);', {"data": item})

    asyncio.get_event_loop().run_until_complete(do())


with DAG(dag_id='posts_transform', default_args=args, schedule_interval=dt.timedelta(minutes=1)) as dag:
    create_posts_dataset = PythonOperator(
        task_id='download_posts_dataset',
        python_callable=download_posts_dataset,
        dag=dag
    )
    transform_posts_dataset = PythonOperator(
        task_id='transform_dataset',
        python_callable=transform_dataset,
        dag=dag
    )
    save_posts_dataset = PythonOperator(
        task_id='save_dataset',
        python_callable=save_dataset,
        dag=dag
    )
    create_posts_dataset >> transform_posts_dataset >> save_posts_dataset

if __name__ == "__main__":
    FILENAME_RAW = os.path.abspath(os.path.join('..', 'result', 'posts_raw.json'))
    FILENAME_PRC = os.path.abspath(os.path.join('..', 'result', 'posts_postprocessing.json'))
    download_posts_dataset()
    transform_dataset()
    save_dataset()
