import os
import re

import numpy as np
import pandas as pd
from src.colors import bcolors
from src.db import close, get_mysql_conn


def csv_to_df(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    print(f"{bcolors.OKGREEN}{csv_path} loaded:{bcolors.ENDC}")
    print(df)
    print()
    print(df.dtypes)
    print("=====================")
    print()

    return df


def load_movies_csv_into_mysql():
    # get the path to the current file
    dirname = os.path.dirname(__file__)

    # get the path of the csv file relative to the current one
    movies_path = os.path.join(dirname, "datasets/imdb_movies.csv")

    df = csv_to_df(movies_path)

    connection = get_mysql_conn()
    cursor = connection.cursor()

    for _, row in df.iterrows():
        # refactor the date field to be able to insert it as date into the database
        # because it's written in a bad format in the csv file
        month, day, year = str(row["date_x"]).strip().split("/")
        row["date_x"] = f"{year}-{month}-{day}"

        # replace all NaN values with None because None can be interpreted by the DB as NULL
        row = row.replace({np.nan: None})

        values = tuple(row)

        query = f"insert into imdb_movies (names, date_x, score, genre, overview, crew, orig_title, status, orig_lang, budget_x, revenue, country) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, values)

    connection.commit()
    close(cursor, connection)


def load_top1000_csv_into_mysql():
    # get the path to the current file
    dirname = os.path.dirname(__file__)

    # get the path of the csv file relative to the current one
    top1000_path = os.path.join(dirname, "datasets/imdb_top_1000.csv")

    df = csv_to_df(top1000_path)

    connection = get_mysql_conn()
    cursor = connection.cursor()

    for _, row in df.iterrows():

        # replace all NaN values with None because None can be interpreted by the DB as NULL
        row = row.replace({np.nan: None})

        # convert "123,456" values to 123456
        row["Gross"] = int(str(row["Gross"]).replace(
            ",", "")) if row["Gross"] != None else row["Gross"]

        # there's wrong data in the CSV and on some records in released year, the rating value is written.
        # Wrong values are replaced with None
        row["Released_Year"] = None if not re.match(
            r"\b\d+\b", row["Released_Year"]) else row["Released_Year"]

        values = tuple(row)

        query = f"insert into imdb_top_1000 (poster_link, series_title, released_year, certificate, runtime, genre, imdb_rating, overview, meta_score, director, star1, star2, star3, star4, no_of_votes, gross) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, values)

    connection.commit()
    close(cursor, connection)


def load_netflix_shows_into_mysql():
    # get the path to the current file
    dirname = os.path.dirname(__file__)

    netflix_path = os.path.join(
        dirname, "datasets/Netflix TV Shows and Movies.csv")

    df = csv_to_df(netflix_path)

    # we don't need the index column, we have an id column
    df = df.drop(columns=["index"])

    connection = get_mysql_conn()
    cursor = connection.cursor()

    for _, row in df.iterrows():
        # replace all NaN values with None because None can be interpreted by the DB as NULL
        row = row.replace({np.nan: None})

        values = tuple(row)
        query = f"insert into netflix_shows_and_movies values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, values)

    connection.commit()
    close(cursor, connection)
