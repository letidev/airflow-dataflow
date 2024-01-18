import datetime

from src.csv_to_mysql import (load_movies_csv_into_mysql,
                              load_netflix_shows_into_mysql,
                              load_top1000_csv_into_mysql)
from src.db import (create_mysql_tables, create_pg_tables, drop_mysql_tables,
                    drop_pg_tables)
from src.mysql_to_postgres import (mysql_movies_to_pg, mysql_netflix_to_pg,
                                   mysql_top1000_to_pg)

from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator


@dag(dag_id="data_flow", start_date=datetime.datetime(2024, 1, 17), schedule="@daily")
def data_flow():
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    download_movies = BashOperator(
        task_id="download_movies",
        bash_command="kaggle datasets download -d harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows -p ./src/datasets --unzip"
    )

    download_top_1000 = BashOperator(
        task_id="download_top1000",
        bash_command="kaggle datasets download -d ashpalsingh1525/imdb-movies-dataset -p ./src/datasets --unzip"
    )

    download_netflix = BashOperator(
        task_id="download_netflix",
        bash_command="kaggle datasets download -d thedevastator/netflix-imdb-scores -p ./src/datasets --unzip"
    )

    @task()
    def drop_mysql_tables_task():
        drop_mysql_tables()

    @task()
    def create_mysql_tables_task():
        create_mysql_tables()

    @task()
    def movies_csv_to_mysql_task():
        load_movies_csv_into_mysql()

    @task()
    def top1000_csv_to_mysql_task():
        load_top1000_csv_into_mysql()

    @task()
    def netflix_csv_to_mysql_task():
        load_netflix_shows_into_mysql()

    @task()
    def drop_pg_tables_task():
        drop_pg_tables()

    @task()
    def create_pg_tables_task():
        create_pg_tables()

    @task()
    def mysql_movies_to_pg_task():
        mysql_movies_to_pg()

    @task
    def mysql_top1000_to_pg_task():
        mysql_top1000_to_pg()

    @task
    def mysql_netflix_to_pg_task():
        mysql_netflix_to_pg()

    start >> [download_movies, download_top_1000, download_netflix] >> drop_mysql_tables_task() >> create_mysql_tables_task() >> [movies_csv_to_mysql_task(
    ), top1000_csv_to_mysql_task(), netflix_csv_to_mysql_task()] >> drop_pg_tables_task() >> create_pg_tables_task() >> [mysql_movies_to_pg_task(), mysql_top1000_to_pg_task(), mysql_netflix_to_pg_task()] >> end


data_flow()
