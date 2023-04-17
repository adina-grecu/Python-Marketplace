"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """

        # init producer variables
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        super().__init__(**kwargs)

    def run(self):

        #register producer 
        producer_id = self.marketplace.register_producer()
        
        while True:
            #for each product, publish it until quantity is reached
            for product in self.products:
                products_left = product[1]
                while products_left > 0:
                    new = self.marketplace.publish(producer_id, product[0])

                    #if there is no space on producer's shelf, wait and try again
                    if new is False:
                        time.sleep(self.republish_wait_time)

                    #if product is published, decrease quantity and wait for production time    
                    else:
                        products_left -= 1
                        time.sleep(product[2])
