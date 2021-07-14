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

A sales order is a record that a customer can use to initiate or request a sale. In general, the sales order is filled out by the customer to order certain products from a business. The customer pays for these products when they submit the sales order. This document represents the promise that the requested goods will be ordered by the business and delivered to the customer later.

When the goods are fulfilled and picked up by the customer, the sales order is used as a receipt to make sure the correct amount and types of products are given to the customer. In simple terms, a sales order is a request from a customer for specific items. 


1. When is a discount generated for a specific user and sales order?
  - If the user is using coupon or promotional codes, then, the discount record will exist before the sale order is being generated
3. second


