# Cargill - Prescreening Tasks for Data Engineer

This document provides the exercises that are part of the prescreening process for Data Engineering
positions. As such, their goal is to provide insights into solutioning process and skills application for
solving example tasks related to this position. Thus, please make sure to explain the important details
and specify any assumption taken.

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

# Exercise 2
Implement the solution above, preferably using Python (with Pandas), Java, C#, or another programming language. You can also use a pseudo-code instead. Please make sure to provide comments where needed to the solution provided.


