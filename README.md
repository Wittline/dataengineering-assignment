# Cargill - Prescreening Tasks for Data Engineer

This document provides the exercises that are part of the prescreening process for Data Engineering positions. As such, their goal is to provide insights into solutioning process and skills application for solving example tasks related to this position. Thus, please make sure to explain the important details and specify any assumption taken.

## Exercise 1
Assume having a Sales table with the following fields:

- Sales Order ID
- Sales Order Item
- Customer ID
- Date
- Transaction Value

And another table named Discounts with the following structure:

- Sales Order ID
- Customer ID
- Discount Value

For a customer and a sales order there can exist a discount value in the Discounts table, however there is no information about the precise discount value per each item in the Sales table. Thus, for this exercise it is necessary to:

- Define Create Table statements for both tables.
- Define a strategy to allocate the discount values to the Sales table (e.g., in a new column) and define the necessary query/scripts to execute the logic.
- Consider different scenarios/edge cases (e.g., depending on the data quality) and, optionally, propose possible solutions and/or scripts to handle such cases.

## Exercise 2
Implement the solution above, preferably using Python (with Pandas), Java, C#, or another programming language. You can also use a pseudo-code instead. Please make sure to provide comments where needed to the solution provided.

# Assumptions
I will assume that this is an e-commerce app, and due to the description of the problem **this is a design problem of an OLTP system**, the exercises are not asking about agregations, data ingestion, transformations and less how to move data between systems, in order to get insights from the preexisted data, there are no references neither of the velocity of the data nor about the tasks scheduled, all the situations mentioned before are features of the OLAP solutions, Hence, **I will avoid based my decisions thinking in OLAP systems.**

A sales order is a record that a customer can use to initiate or request a sale. In general, the sales order is filled out by the customer to order certain products from a business. The customer pays for these products when they submit the sales order. This document represents the promise that the requested goods will be ordered by the business and delivered to the customer later. When the goods are fulfilled and picked up by the customer, the sales order is used as a receipt to make sure the correct amount and types of products are given to the customer. In simple terms, a sales order is a request from a customer for specific items.

There are two relevant situations in the description:

- **For a customer and a sales order there can exist a discount value in the Discounts table**
  - This is let me understand that only a general discount value could be applied to the whole value of the order
  - Are the discounts being generated for a specific users?
  - There are situations where the order can be applied coupons or promotional codes which assign a general discount to the entire purchase.
- **However there is no information about the precise discount value per each item in the Sales table.**
  - Here , the description is taking into account assign different discount vaues per item, which could implied store that information in another table.
  - Is there a catalog with a different discount for each item or is the discount allocation established in a general way to the entire user's order?

## Base case
The initial data model allows assigning a discount per user to each purchased item that appears in the sales table, but there are two problems with this approach:

1. You cannot add different discounts to each item
2. You cannot add more than one item of the same type to the order, this would create a problem with the composite primary key.

![initial](https://user-images.githubusercontent.com/8701464/125843250-e545b578-dc04-41b9-a3ca-a5e22d72b060.png)

let's focus in the relevant tables using PostgreSQL

 ```SQL

CREATE TABLE IF NOT EXISTS Sales(
    sales_order_id int NOT NULL,
    sales_order_item int NOT NULL, 
    customer_id int null,
    date timestamp not null, 
    transaction_value float not null, 
    discounted_value float not null,
    PRIMARY KEY(sales_order_id, sales_order_item, customer_id)
);


CREATE TABLE IF NOT EXISTS Discounts(
    sales_order_id int not null,
    customer_id int not null,
    discount_value float not null
    PRIMARY KEY(sales_order_id, customer_id)
);

insert into sales values 
(1, 2, 150, NOW(), 200, 200),
(1, 3, 150, NOW(), 310, 310),
(1, 4, 150, NOW(), 80, 80)


insert into discounts values (1, 150, 0.3)

```

 ```SQL
select * from sales
```


![image](https://user-images.githubusercontent.com/8701464/125846226-9a106ea3-e8fe-42e0-98fa-d651ee8bd5cb.png)

 ```SQL
select * from discounts
```

![image](https://user-images.githubusercontent.com/8701464/125846290-a12a143d-766c-4738-ba8b-57a6749a01e1.png)

 ```SQL
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
```


 ```SQL
select * from sales
```

![image](https://user-images.githubusercontent.com/8701464/125846332-46ab78ca-3227-444b-b82e-3189b87c60ce.png)



## Edge case
The second approach (edge case), considered add more than the same product to the order and create different discounts to each item.

![second](https://user-images.githubusercontent.com/8701464/125843261-a78879e1-528b-4931-9598-d76d5d57e1f1.png)


