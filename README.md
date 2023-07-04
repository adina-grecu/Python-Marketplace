
The marketplace operates as a simulated store with shelves where producers place their products, and consumers make purchases.

Efficiency was ensured by performing actions in parallel and minimizing interdependencies. However, there is room for improvement as the program retains and iterates through unnecessary information, impacting performance. For example, product details are currently unused. Future development could consider factors such as product prices and consumer budgets when placing orders.


The marketplace serves as an intermediary between consumers and producers, storing the entire market structure. The market consists of shelves owned by producers, which hold their respective products. Actions such as publish, add_to_cart, and remove_from_cart occur between the market and the carts, where consumer shopping carts are stored.

Shelf size is standardized (queue_size_per_producer), and producers can only add products if the shelf size is not exceeded. To validate this restriction, the shelf occupancy level is tracked in shelf_sizes. Available space on a shelf is decremented during publish and remove operations and incremented during add_to_cart.

One challenge encountered during implementation was within the remove function. To update the shelf occupancy consistently, a removed product must return to its original shelf. To address this, an association between the product and its shelf is retained for each product added to a cart.

The producer ttempts to place all products from their list on the shelf using the publish method, one by one, in the specified quantity. A while loop ensures all products are published, and the quantity is updated only if the publish action is successful (as opposed to using a for loop since there can be multiple publish attempts).

The consumer requests a cart from the marketplace to begin shopping, using the init_cart method. To ensure data integrity, namely that products are added and removed as required, the same logic as the producer is followed. A while loop updates the quantity when the add action is successfully completed (also for remove). Once all actions for a cart are completed, the order is placed by calling the place_order function, and the process continues with the next cart in the list until the end.

An order is placed after the cart's contents are taken to the checkout counter and the cart is returned. This is represented in the program by moving the cart's contents to an "order" variable and removing the cart from the carts dictionary.

A special case considered is when a consumer tries to remove a non-existent product from the cart. Although a check for this situation is implemented, it is not reflected in the tests.

Resources Used

Logger: Implemented logging using RotatingFileHandler and referenced Python's official logging documentation.

Unit Testing: Utilized Python's built-in unittest library for unit testing.
