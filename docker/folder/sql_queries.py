# DROP TABLES

sales_table_drop = "DROP TABLE IF EXISTS Sales"
customers_table_drop = "DROP TABLE IF EXISTS Customers"
products_table_drop = "DROP TABLE IF EXISTS Products"
suppliers_table_drop = "DROP TABLE IF EXISTS Suppliers"
discounts_table_drop = "DROP TABLE IF EXISTS Discounts"


# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays(
    songplay_id serial PRIMARY KEY,
    start_time bigint NOT NULL, 
    user_id int null,
    level varchar(255) not null, 
    song_id varchar(255) null,
    artist_id varchar(255) null, 
    session_id int NOT NULL, 
    location varchar(255),
    user_agent varchar(255)
);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users(
    user_id varchar(255) PRIMARY KEY,
    first_name varchar(255),
    last_name varchar(255),
    gender char,
    level varchar(255) not null
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs(
    song_id varchar(255) PRIMARY KEY,
    title varchar(255) not null,
    artist_id varchar(255) not null,
    year int not null,
    duration float not null
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (

    artist_id varchar(255) PRIMARY KEY,
    name varchar(255) not null,
    location varchar(255) not null,
    latitude real  null,
    longitude real  null
    
);
""")

time_table_create = ("""

CREATE TABLE IF NOT EXISTS time (
    start_time timestamp PRIMARY KEY, 
    hour int not null, 
    day int not null, 
    week int not null, 
    month int not null, 
    year int not null, 
    weekday int not null
    
);

""")

# INSERT RECORDS

songplay_table_insert = ("""
    insert into songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    values  (%s,%s,%s,%s,%s,%s,%s,%s);
""")

user_table_insert = ("""
    insert into users (user_id, first_name, last_name, gender, level)
    values  (%s,%s,%s,%s,%s)
    ON CONFLICT(user_id) DO update
       SET first_name = excluded.first_name,
           last_name = excluded.last_name,
           gender = excluded.gender,
           level = excluded.level;           
""")

song_table_insert = ("""
    insert into songs (song_id, title, artist_id, year, duration)
    values  (%s,%s,%s,%s,%s)
    ON CONFLICT do nothing;
""")

artist_table_insert = ("""
    insert into artists (artist_id, name, location, latitude, longitude)
    values  (%s,%s,%s,%s,%s)
    ON CONFLICT do nothing;
""")


time_table_insert = ("""
    insert into time (start_time, hour, day, week, month, year, weekday)
    values  (%s,%s,%s,%s,%s,%s,%s)
    ON CONFLICT do nothing;
""")

# FIND SONGS

song_select = ("""
SELECT so.song_id, ar.artist_id 
FROM songs AS so
LEFT OUTER JOIN artists AS ar ON so.artist_id = ar.artist_id
where so.title = %s AND ar.name = %s and so.duration = %s;
""")


create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [sales_table_drop, customers_table_drop, products_table_drop, suppliers_table_drop, discounts_table_drop]