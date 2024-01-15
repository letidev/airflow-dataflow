import datetime

from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator


@dag(dag_id="first_dag", start_date=datetime.datetime(2024, 1, 14), schedule="@daily")
def first_dag():

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    @task()
    def print_message():
        print("Hello Airflow!")

    start >> print_message() >> end


first_dag()
