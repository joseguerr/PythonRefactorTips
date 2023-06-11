Let’s use the example of a company that produces and sells car parts to different customers.

The following ETL job receives customers’ orders and a list of car parts as .csv files and must create three outputs:

1 - A file containing the initial customers' orders, enriched with total volume for each order and the factory where the order will be sent out.

2 - A file containing all orders' items split into separate rows, associated with a rank. The file should contain the order id, the rank of the item within the order and the item code. The rank does not need to follow any specific order.

3 - A file containing the number of times each car part has been ordered.

The car parts are described by a unique code_id, car_type (SUV, Sedan, Van, Sports Car), dimensions, shape, quantity and price.
The orders are described by a delivery day, an order id, a customer id and the multiple code id of the car parts present in the order.

There are 3 factories: Forge Works, Meltdown Manufacturing, Radiant Rims. Each Factory accepts orders for specific car types, as follows:
Factory Forge Works accepts SUV orders
Factory Meltdown Manufacturing accept Sedan orders
Factory Radiant Rims accepts Van + Sports Car orders

For file 1, customers' orders must be sorted by ascending delivery date and within each delivery day the following factory order must be respected:
1 - Meltdown Manufacturing
2 - Radiant Rims
3 - Forge Works
