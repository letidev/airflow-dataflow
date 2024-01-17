import os

import mysql.connector
import psycopg2
from dotenv import load_dotenv
from src.colors import bcolors


def get_mysql_conn():
    load_dotenv()
    mysql_conn = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        port=os.getenv('MYSQL_PORT'),
        database=os.getenv('MYSQL_DATABASE_NAME'),
        user=os.getenv('MYSQL_ROOT_USER'),
        password=os.getenv('MYSQL_ROOT_PASSWORD')
    )
    print(f"{bcolors.OKCYAN}mysql conn - {mysql_conn}{bcolors.ENDC}")
    return mysql_conn


def get_pg_conn():
    load_dotenv()
    pg_conn = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT'),
        database=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD')
    )

    print(f"{bcolors.FAIL}postgres conn - {pg_conn}{bcolors.ENDC}")
    return pg_conn
