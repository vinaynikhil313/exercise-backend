### Decisions & Assumptions
- Orders are not tied to any users at the moment based on the pre-defined structure of `CreateOrderModel`.
- A relational (PostgreSQL) database is chosen to help with the consistency of the application and for performing any additional queries in the future on order data.
- The placement of order will be tried `once` as soon as the order is created in our database. This can be easily changed to remove this `synchronous` order placement and defer it to the background process.
- If order creation is successful and the order is placed in the stock market successfully, then the order is returned with the 201 code and `SUCCESS` status.
- If the order is created on our system but fails to be placed in the stock market, the API does not wait for the order to be successfully placed. It returns with a 201 code and `IN PROGRESS` status and the placement is retried (asynchronously) upto 5 times in the stock exchange.
- If the order placement fails even after retries, then the order is marked as a `FAILURE` in the database.
- If there are any issues with the order being created in our database in the first place, then the API returns a 500 status code with the given error message.
- A background process is chosen for retries as the volume of failure itself shouldn't be very high. The API would respond irrespective of the reliability/failures of the stock market.
- In terms of scalability, and the entire service can be scaled horizontally in response to heavy loads. The database can also be scaled up vertically or horizontally (using read/write instances, partitions and shards) to adapt to heavy loads.
- The scaled up instances will also be able to handle stock market failures independently.

### Instructions to run
- The entire application along with the database is dockerized. A docker-compose file is provided to easily setup and run the application.
```commandline
docker-compose up --build
```

### Future improvements
- Adding a background service that checks and reports any FAILED orders. It could also be an external service which can be called or listens to messages in case of failed orders.
- In case of high volume of async updates to the orders placed through a socket connection on the stock exchange, a simple solution could be to track them (order_id, stock_market_order_status) in a separate table so that there is no impact on the functioning of the REST API itself and these both processes can be run independently within the same service or in different services. 