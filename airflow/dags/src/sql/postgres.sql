create table imdb_movies (
  id serial primary key,
  names text,
  date_x date,
  score smallint,
  genre varchar(512),
  overview text,
  crew text,
  orig_title varchar(512),
  status varchar(64),
  orig_lang varchar(64),
  budget_x decimal(12,2),
  revenue decimal(12,2),
  country varchar(4)
);

create table imdb_top_1000 (
  id serial primary key,
  poster_link varchar(1024),
  series_title varchar(256),
  released_year int,
  certificate varchar(8),
  runtime varchar(16),
  genre text,
  imdb_rating decimal(3, 1),
  overview text,
  meta_score int,
  director varchar(256),
  star1 varchar(128),
  star2 varchar(128),
  star3 varchar(128),
  star4 varchar(128),
  no_of_votes bigint,
  gross int
);

CREATE TYPE movie_type AS ENUM ('MOVIE', 'SHOW');

create table netflix_shows_and_movies (
	id varchar(32) not null unique primary key,
	title varchar(256),
	movie_type movie_type,
	description text,
	release_year int,
	age_certification varchar(8),
	runtime int,
	imdb_id varchar(32),
	imdb_score decimal(3, 1),
	imdb_votes bigint
)

select * from imdb_movies;
select * from imdb_top_1000;
select * from netflix_shows_and_movies;

drop table if exists imdb_movies; 
drop table if exists imdb_top_1000; 
drop table if exists netflix_shows_and_movies;