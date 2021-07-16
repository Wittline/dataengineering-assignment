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
The second approach (edge case), considered add more than one unit of the same product to the order (quantity) and create different discounts to each item, and update the discount is less complex

![second](https://user-images.githubusercontent.com/8701464/125843261-a78879e1-528b-4931-9598-d76d5d57e1f1.png)


 ```SQL

CREATE TABLE IF NOT EXISTS Sales2(
    sales_order_id int NOT NULL,
    customer_id int null,
    date timestamp not null, 
    PRIMARY KEY(sales_order_id, customer_id)
);

CREATE TABLE IF NOT EXISTS Order_detail(
    sales_order_id int not null,
    sales_order_item int NOT NULL, 
    transaction_value float not null,
    quantity int not null, 
    discount_value float not null,
    discounted_value float not null,
    PRIMARY KEY(sales_order_id, sales_order_item)
);


insert into Sales2 values (1, 150, NOW())

insert into Order_detail values 
(1, 2, 150, 2, 0.3, 150),
(1, 3, 210, 1, 0.4, 210), 
(1, 4, 80, 3, 0.2, 80)


```

 ```SQL
select * from sales2
```


![image](https://user-images.githubusercontent.com/8701464/125873099-70979ace-318f-4e1b-adb9-3abb5a73e1d5.png)


 ```SQL
select * from Order_detail
```

![image](https://user-images.githubusercontent.com/8701464/125873136-2604e75f-13db-4eb6-832a-8f193d50c3b0.png)


 ```SQL
UPDATE Order_detail
SET discounted_value = (transaction_value - (transaction_value * discount_value)) * quantity
WHERE sales_order_id = %s

```

 ```SQL
select * from Order_detail
```

![image](https://user-images.githubusercontent.com/8701464/125873152-5de4f628-fe3a-4af0-82ca-c70c182d8fc3.png)


 # Steps to execute the project

 - Install <a href="https://docs.docker.com/docker-for-windows/install/">Docker Desktop on Windows</a>, it will install **docker compose** as well, docker compose will alow you to run multiple containers applications, this project has two containers with **Jupyter Notebook** and **PostgreSQL**

- Install <a href="https://www.stanleyulili.com/git/how-to-install-git-bash-on-windows/">git-bash for windows</a>, once installed , open **git bash** and download this repository, this will download all the folders and the **docker-compose.yml** file, and other files needed.

``` 
ramse@DESKTOP-K6K6E5A MINGW64 /c
$ git clone https://github.com/Wittline/cargill-assignment.git
```

- Once all the files needed were downloaded from the repository , Let's run everything we will use the git bash tool again, go to the folder *~/documents/github/cargill-assignment/docker* and run the docker compose command

``` 
ramse@DESKTOP-K6K6E5A MINGW64 ~/documents/github/cargill-assignment/docker (main)
$ docker-compose up
``` 
let's wait until all the images and containers are created

![image](https://user-images.githubusercontent.com/8701464/125874773-b4796bd0-11c4-4575-aa0c-ecdeae9f9f07.png)

- Open a new git bash window again, and use the following command:

``` 
ramse@DESKTOP-K6K6E5A MINGW64 ~/documents/github/cargill-assignment/docker (main)
$ docker ps
```
It will show you all the containers and images contained in the **docker-compose-yml** file, this mean that all the images were created correctly

![image](https://user-images.githubusercontent.com/8701464/125874919-7ba20efa-1070-45f1-8692-f5e4379f0bba.png)

let's check the **docker-compose.yml** file 
``` 
version: '3'

services:
    jupyter-notebook:
        image: jupyter/minimal-notebook
        volumes:
            - ./folder:/home/jovyan/work
        ports:
            - 8888:8888
        container_name: jupyter-notebook-container
        environment:
            - JUPYTER_TOKEN=cargill
        command: jupyter notebook --NotebookApp.iopub_data_rate_limit=3e10
        depends_on:
            - "db"
    db:
        container_name: pg_container
        image: postgres
        restart: always
        environment:
            POSTGRES_USER: "cargill"
            POSTGRES_PASSWORD: "cargill"
            POSTGRES_DB: "cargill_db"
        ports:
            - "5432:5432"
        volumes:
            - pg_data:/var/lib/postgresql/data/

volumes:
    pg_data:
```

- go to the url **http://localhost:8888/** the psw will be **cargill** putted in the tag **- JUPYTER_TOKEN=cargill**

![image](https://user-images.githubusercontent.com/8701464/125875400-1af2e8e9-ade4-4d91-9f3c-92ae700f91a2.png)

The jupyter notebook of this project is called **cargill-assignment.ipynb** over the folder **work**

![image](https://user-images.githubusercontent.com/8701464/125875448-22edece7-e787-4052-98f0-81dd6026c25d.png)

Now you can run the project step by step using this notebook, the files **sql_queries.py** and **db_engine.py** contains all the logic needed

![image](https://user-images.githubusercontent.com/8701464/125875577-fda57bf9-0d18-4508-b98b-5c681dff2425.png)


![image](https://user-images.githubusercontent.com/8701464/125873180-d7d970df-fe2b-4a96-a1dd-417a49e12b66.png)






