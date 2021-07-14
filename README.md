# Cargill - Prescreening Tasks for Data Engineer

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

For a customer and a sales order there can exist a discount value in the Discounts table, however there
is no information about the precise discount value per each item in the Sales table. Thus, for this
exercise it is necessary to:

a) Define Create Table statements for both tables.
b) Define a strategy to allocate the discount values to the Sales table (e.g., in a new column)
and define the necessary query/scripts to execute the logic.
c) Consider different scenarios/edge cases (e.g., depending on the data quality) and,
optionally, propose possible solutions and/or scripts to handle such cases.


