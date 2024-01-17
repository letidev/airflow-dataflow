import datetime

from src.csv_to_mysql import (load_movies_csv_into_mysql,
                              load_netflix_shows_into_mysql,
                              load_top1000_csv_into_mysql)

from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator


@dag(dag_id="data_flow", start_date=datetime.datetime(2024, 1, 17), schedule="@daily")
def data_flow():
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    @task()
    def movies_csv_to_mysql():
        load_movies_csv_into_mysql()

    @task()
    def top1000_csv_to_mysql():
        load_top1000_csv_into_mysql()

    @task()
    def netflix_csv_to_mysql():
        load_netflix_shows_into_mysql()

    start >> [movies_csv_to_mysql(), top1000_csv_to_mysql(),
              netflix_csv_to_mysql()] >> end


data_flow()
