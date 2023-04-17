"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """

        #init consumer variables
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        super().__init__(**kwargs)

    def run(self):

        #for each cart, get a new cart id
        for cart in self.carts:
            cart_id = self.marketplace.new_cart()

            #for each product in cart, check the type of action and perform it
            for product in cart:
                if product["type"] == "add":
                    products_left = product["quantity"]

                    #add product to cart until quantity is reached
                    while products_left > 0:
                        new = self.marketplace.add_to_cart(cart_id, product["product"])

                        #if product is not found in marketplace, wait and try again
                        if new is False:
                            time.sleep(self.retry_wait_time)

                        else:
                            products_left -= 1

                elif product["type"] == "remove":
                    products_left = product["quantity"]

                    #remove product from cart until quantity is reached
                    while products_left > 0:
                        new = self.marketplace.remove_from_cart(cart_id, product["product"])

                        #if product is not found in cart, wait and try again
                        if new is False:
                            time.sleep(self.retry_wait_time)

                        else:
                            products_left -= 1    

            self.marketplace.place_order(cart_id)
