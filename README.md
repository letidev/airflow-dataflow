# Python Version

3.11

# Datasets

The datasets in this project are downloaded through kaggle's API but not by hand, they are run as bash tasks in airflow. To download them by hand, run the following commands:

```bash
kaggle datasets download -d harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows -p ./airflow/dags/src/datasets --unzip
```

```bash
kaggle datasets download -d ashpalsingh1525/imdb-movies-dataset -p ./airflow/dags/src/datasets --unzip
```

```bash
kaggle datasets download -d thedevastator/netflix-imdb-scores -p ./airflow/dags/src/datasets --unzip
```

# Configuration

In `.env` configure the following variables:

```
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=

MYSQL_HOST=
MYSQL_PORT=
MYSQL_ROOT_USER=
MYSQL_ROOT_PASSWORD=
MYSQL_DATABASE_NAME=
```

In `.envrc` configure the following ones. These are used to configure the airflow installation, set up in the environment its home directory and also to configure in the environment kaggle's API username and key which are needed when downloading datasets:

```
# airflow config
export AIRFLOW_HOME="${PWD}/airflow"
export AIRFLOW_VERSION=2.8.0
export PYTHON_VERSION=3.11
export CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

# kaggle api config
export KAGGLE_USERNAME=
export KAGGLE_KEY=
```

Make sure to run `direnv allow` every time you make changes to `.envrc`.
