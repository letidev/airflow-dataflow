import os

import mysql.connector
import psycopg2
from dotenv import load_dotenv

from colors import bcolors

load_dotenv()

mydb = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST'),
    port=os.getenv('MYSQL_PORT'),
    database=os.getenv('MYSQL_DATABASE_NAME'),
    user=os.getenv('MYSQL_ROOT_USER'),
    password=os.getenv('MYSQL_ROOT_PASSWORD')
)

postgresdb = psycopg2.connect(
    host=os.getenv('POSTGRES_HOST'),
    port=os.getenv('POSTGRES_PORT'),
    database=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD')
)

print(f"{bcolors.OKCYAN}mysql conn - {mydb}{bcolors.ENDC}")
print(f"{bcolors.FAIL}postgres conn - {postgresdb}{bcolors.ENDC}")
