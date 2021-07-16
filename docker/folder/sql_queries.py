# DROP TABLES

sales_table_drop = "DROP TABLE IF EXISTS Sales"
discounts_table_drop = "DROP TABLE IF EXISTS Discounts"
sales2_table_drop = "DROP TABLE IF EXISTS Sales2"
order_detail_table_drop = "DROP TABLE IF EXISTS Order_detail"


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


sales2_table_create = ("""
CREATE TABLE IF NOT EXISTS Sales2(
    sales_order_id int NOT NULL,
    customer_id int null,
    date timestamp not null, 
    PRIMARY KEY(sales_order_id, customer_id)
);
""")

order_detail_table_create = ("""
CREATE TABLE IF NOT EXISTS Order_detail(
    sales_order_id int not null,
    sales_order_item int NOT NULL, 
    transaction_value float not null,
    quantity int not null, 
    discount_value float not null,
    discounted_value float not null,
    PRIMARY KEY(sales_order_id, sales_order_item)
);
""")

# # INSERT RECORDS

sales_insert = ("""
insert into Sales values (1, 2, 150, NOW(), 200, 200),(1, 3, 150, NOW(), 310, 310),(1, 4, 150, NOW(), 80, 80)
""")

discounts_insert = ("""
    insert into Discounts values (1, 150, 0.3)
""")

sales2_insert = ("""
insert into Sales2 values (1, 150, NOW())
""")

order_detail_insert = ("""
    insert into Order_detail values (1, 2, 150, 2, 0.3, 150), (1, 3, 210, 1, 0.4, 210), (1, 4, 80, 3, 0.2, 80)
""")

# # INSERT TABLES

sales_update = (
"""
WITH sales_updated_CTE(sales_order_id,sales_order_item, customer_id, date,transaction_value, discount)
AS
(
    SELECT 
        s.sales_order_id,
        s.sales_order_item,
        s.customer_id,
        s.date,
        s.transaction_value,
        (s.transaction_value - (s.transaction_value * d.discount_value)) AS discount
    FROM sales s
    JOIN discounts d
    ON s.sales_order_id = d.sales_order_id
    WHERE s.sales_order_id = %s AND s.customer_id = %s
)
UPDATE sales as s
SET discounted_value = c.discount
FROM sales_updated_CTE as c 
WHERE c.sales_order_id = s.sales_order_id 
AND c.customer_id = s.customer_id
AND c.sales_order_item = s.sales_order_item
"""
)

order_detail_update = (
"""
UPDATE Order_detail
SET discounted_value = (transaction_value - (transaction_value * discount_value)) * quantity
WHERE sales_order_id = %s
"""
)



update_identifier = {'sales': sales_update, 'order_detail': order_detail_update}
insert_table_queries = [sales_insert,discounts_insert,sales2_insert, order_detail_insert]
create_table_queries = [sales_table_create, discounts_table_create, sales2_table_create, order_detail_table_create]
drop_table_queries = [sales_table_drop, discounts_table_drop, sales2_table_drop, order_detail_table_drop]