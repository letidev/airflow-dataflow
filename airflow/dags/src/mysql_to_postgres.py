import pandas as pd
from src.db import close, get_mysql_conn, get_pg_conn


def mysql_to_df(table_name) -> pd.DataFrame:
    mysql_conn = get_mysql_conn()
    mysql_cursor = mysql_conn.cursor()

    # load mysql table to pandas DF
    query = f"select * from {table_name}"
    mysql_cursor.execute(query)
    rows = mysql_cursor.fetchall()
    columns = [col[0] for col in mysql_cursor.description]

    # close mysql connection
    close(mysql_cursor, mysql_conn)
    return pd.DataFrame(rows, columns=columns)


def df_to_pg(df, table_name):
    pg_conn = get_pg_conn()
    pg_cursor = pg_conn.cursor()

    # the number of params extracted from the
    # number of columns in the dataframe
    params = ",".join([f"%s"] * df.shape[1])

    # generate an insert statement for each row
    for _, row in df.iterrows():
        values = tuple(row)
        query = f"insert into {table_name} values ({params})"
        pg_cursor.execute(query, values)

    pg_conn.commit()
    close(pg_cursor, pg_conn)


def mysql_movies_to_pg():
    table_name = "imdb_movies"
    df = mysql_to_df(table_name)

    # postgres, unlike mysql, can't store NaN or Null in numeric columns
    df = df.fillna(0)

    df_to_pg(df, table_name)


def mysql_top1000_to_pg():
    table_name = "imdb_top_1000"
    df = mysql_to_df(table_name)

    # postgres, unlike mysql, can't store NaN or Null in numeric columns
    df = df.fillna(0)

    # fix wrong wrong column types
    df = df.astype(
        {"released_year": "int16", "meta_score": "int16", "gross": "int16"})

    df_to_pg(df, table_name)


def mysql_netflix_to_pg():
    table_name = "netflix_shows_and_movies"
    df = mysql_to_df(table_name)

    # postgres, unlike mysql, can't store NaN or Null in numeric columns
    df = df.fillna(0)

    df_to_pg(df, table_name)
