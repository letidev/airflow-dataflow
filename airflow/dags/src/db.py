import os

import mysql.connector
import psycopg2
from dotenv import load_dotenv
from src.colors import bcolors


def close(cursor, connection):
    cursor.close()
    print("closed mysql cursor")
    connection.close()
    print("closed mysql connection")


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


def drop_mysql_tables():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    cursor.execute("drop table if exists imdb_movies")
    cursor.execute("drop table if exists imdb_top_1000")
    cursor.execute("drop table if exists netflix_shows_and_movies")
    conn.commit()

    close(cursor, conn)


def drop_pg_tables():
    conn = get_pg_conn()
    cursor = conn.cursor()
    cursor.execute("drop table if exists imdb_movies")
    cursor.execute("drop table if exists imdb_top_1000")
    cursor.execute("drop table if exists netflix_shows_and_movies")
    cursor.execute("drop type if exists movie_type")
    conn.commit()

    close(cursor, conn)


def create_mysql_tables():
    conn = get_mysql_conn()
    cursor = conn.cursor()

    cursor.execute("create table imdb_movies ( \
        id int not null auto_increment, \
        names text, \
        date_x date, \
        score tinyint, \
        genre varchar(512), \
        overview text, \
        crew text, \
        orig_title varchar(512), \
        status varchar(64), \
        orig_lang varchar(64), \
        budget_x decimal(12,2), \
        revenue decimal(12,2), \
        country varchar(4), \
        primary key (id) \
        );")

    cursor.execute("create table imdb_top_1000 ( \
        id int not null auto_increment, \
        poster_link varchar(1024), \
        series_title varchar(256), \
        released_year int, \
        certificate varchar(8), \
        runtime varchar(16), \
        genre text, \
        imdb_rating decimal(3, 1), \
        overview text, \
        meta_score int, \
        director varchar(256), \
        star1 varchar(128), \
        star2 varchar(128), \
        star3 varchar(128), \
        star4 varchar(128), \
        no_of_votes bigint, \
        gross int, \
        primary key (id) \
        );")

    cursor.execute("create table netflix_shows_and_movies ( \
            id varchar(32) not null unique, \
            title varchar(256), \
            movie_type enum('MOVIE', 'SHOW'), \
            description text, \
            release_year int, \
            age_certification varchar(8), \
            runtime int, \
            imdb_id varchar(32), \
            imdb_score decimal(3, 1), \
            imdb_votes bigint, \
            primary key(id) \
        )")

    conn.commit()
    close(cursor, conn)


def create_pg_tables():
    conn = get_pg_conn()
    cursor = conn.cursor()

    cursor.execute("create table imdb_movies ( \
        id serial primary key, \
        names text, \
        date_x date, \
        score smallint, \
        genre varchar(512), \
        overview text, \
        crew text, \
        orig_title varchar(512), \
        status varchar(64), \
        orig_lang varchar(64), \
        budget_x decimal(12,2), \
        revenue decimal(12,2), \
        country varchar(4) \
        )")

    cursor.execute("create table imdb_top_1000 ( \
        id serial primary key, \
        poster_link varchar(1024), \
        series_title varchar(256), \
        released_year int, \
        certificate varchar(8), \
        runtime varchar(16), \
        genre text, \
        imdb_rating decimal(3, 1), \
        overview text, \
        meta_score int, \
        director varchar(256), \
        star1 varchar(128), \
        star2 varchar(128), \
        star3 varchar(128), \
        star4 varchar(128), \
        no_of_votes bigint, \
        gross int \
        );")

    cursor.execute("CREATE TYPE movie_type AS ENUM ('MOVIE', 'SHOW')")

    cursor.execute("create table netflix_shows_and_movies ( \
        id varchar(32) not null unique primary key, \
        title varchar(256), \
        movie_type movie_type, \
        description text, \
        release_year int, \
        age_certification varchar(8), \
        runtime int, \
        imdb_id varchar(32), \
        imdb_score decimal(3, 1), \
        imdb_votes bigint \
        )")

    conn.commit()
    close(cursor, conn)
