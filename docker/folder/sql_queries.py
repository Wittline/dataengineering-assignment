# DROP TABLES

sales_table_drop = "DROP TABLE IF EXISTS Sales"
customers_table_drop = "DROP TABLE IF EXISTS Customers"
products_table_drop = "DROP TABLE IF EXISTS Products"
suppliers_table_drop = "DROP TABLE IF EXISTS Suppliers"
discounts_table_drop = "DROP TABLE IF EXISTS Discounts"


# CREATE TABLES

sales_table_create = ("""
CREATE TABLE IF NOT EXISTS Sales(
    sales_order_id int NOT NULL,
    sales_order_item int NOT NULL, 
    customer_id int null,
    date timestamp not null, 
    transaction_value float not null, 
    discounted_value float not null,
    PRIMARY KEY(sales_order_id, sales_order_item, customer_id)
);
""")

discounts_table_create = ("""
CREATE TABLE IF NOT EXISTS Discounts(
    sales_order_id int not null,
    customer_id int not null,
    discount_value float not null
);
""")

# # INSERT RECORDS

# songplay_table_insert = ("""
#     insert into songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
#     values  (%s,%s,%s,%s,%s,%s,%s,%s);
# """)

# user_table_insert = ("""
#     insert into users (user_id, first_name, last_name, gender, level)
#     values  (%s,%s,%s,%s,%s)
#     ON CONFLICT(user_id) DO update
#        SET first_name = excluded.first_name,
#            last_name = excluded.last_name,
#            gender = excluded.gender,
#            level = excluded.level;           
# """)

# song_table_insert = ("""
#     insert into songs (song_id, title, artist_id, year, duration)
#     values  (%s,%s,%s,%s,%s)
#     ON CONFLICT do nothing;
# """)

# artist_table_insert = ("""
#     insert into artists (artist_id, name, location, latitude, longitude)
#     values  (%s,%s,%s,%s,%s)
#     ON CONFLICT do nothing;
# """)


# time_table_insert = ("""
#     insert into time (start_time, hour, day, week, month, year, weekday)
#     values  (%s,%s,%s,%s,%s,%s,%s)
#     ON CONFLICT do nothing;
# """)

# # FIND SONGS

# song_select = ("""
# SELECT so.song_id, ar.artist_id 
# FROM songs AS so
# LEFT OUTER JOIN artists AS ar ON so.artist_id = ar.artist_id
# where so.title = %s AND ar.name = %s and so.duration = %s;
# """)


create_table_queries = [sales_table_create, discounts_table_create]
drop_table_queries = [sales_table_drop, customers_table_drop, products_table_drop, suppliers_table_drop, discounts_table_drop]