"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Lock, current_thread
import unittest
import logging
from logging.handlers import RotatingFileHandler

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        
        self.logger = logging.getLogger("marketplace_logger")
        self.logger.setLevel(logging.INFO)
        handler = RotatingFileHandler("marketplace.log", maxBytes=100000, backupCount=5)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.info("Marketplace initialized")

        self.queue_size_per_producer = queue_size_per_producer
        self.shelf_sizes = {}
        self.producer_id_generator = 0
        self.market = {}
        self.carts = {}
        self.cart_generator = 0
        self.producer_id_lock = Lock()
        self.cart_lock = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        with self.producer_id_lock:
            self.producer_id_generator += 1
            prod_id = self.producer_id_generator
            self.market[prod_id] = []
            self.shelf_sizes[prod_id] = self.queue_size_per_producer

            self.logger.info("Producer registered with id " + str(prod_id))

            return self.producer_id_generator

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """

        if len(self.market[producer_id]) < self.queue_size_per_producer:
            self.market[producer_id].append(product)
            self.shelf_sizes[producer_id] -= 1

            self.logger.info("Product published: " + str(product))

            return True
        
        self.logger.info("Product not published: " + str(product))

        return False
        

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        with self.cart_lock:
            self.cart_generator += 1
            self.carts[self.cart_generator] = []

            self.logger.info("New cart created with id " + str(self.cart_generator))

            return self.cart_generator


    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """

        for shelf in self.market:
            if product in self.market[shelf]:
                self.market[shelf].remove(product)
                self.carts[cart_id].append(product)
                self.shelf_sizes[shelf] += 1

                self.logger.info("Product added to cart: " + str(product))

                return True
            
        self.logger.info("Product not found in market: " + str(product))    

        return False

        


    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """

        if(product in self.carts[cart_id]):
            self.carts[cart_id].remove(product)

            self.logger.info("Product removed from cart: " + str(product))

            return True
        
        self.logger.info("Product not found in cart: " + str(product))

        return False
            

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        order = self.carts[cart_id]
        self.carts[cart_id] = []
        self.carts.pop(cart_id)
        
        for product in order:
            print(current_thread().name, "bought", product)

        self.logger.info("Order placed: " + str(order))

        return order
    
class TestMarketplace(unittest.TestCase):

    def setUp(self):
        self.marketplace = Marketplace(2)

    def test_register_producer(self):
        producer_id_1 = self.marketplace.register_producer()    
        producer_id_2 = self.marketplace.register_producer()
        self.assertEqual(producer_id_1, 1)  
        self.assertEqual(producer_id_2, 2)   

    def test_publish(self):
        producer_id = self.marketplace.register_producer()
        self.assertEqual(self.marketplace.publish(producer_id, "product1"), True)
        self.assertEqual(self.marketplace.publish(producer_id, "product2"), True)
        self.assertEqual(self.marketplace.publish(producer_id, "product3"), False)

    def test_new_cart(self):
        cart_id = self.marketplace.new_cart()
        self.assertEqual(cart_id, 1)

    def test_add_to_cart(self):
        producer_id = self.marketplace.register_producer()
        self.marketplace.publish(producer_id, "product1")
        self.marketplace.publish(producer_id, "product2")
        cart_id = self.marketplace.new_cart()
        self.assertEqual(self.marketplace.add_to_cart(cart_id, "product1"), True)
        self.assertEqual(self.marketplace.add_to_cart(cart_id, "product2"), True)
        self.assertEqual(self.marketplace.add_to_cart(cart_id, "product3"), False)     

    def test_remove_from_cart(self):
        producer_id = self.marketplace.register_producer()
        self.marketplace.publish(producer_id, "product1")
        self.marketplace.publish(producer_id, "product2")
        cart_id = self.marketplace.new_cart()
        self.marketplace.add_to_cart(cart_id, "product1")
        self.marketplace.add_to_cart(cart_id, "product2")
        self.assertEqual(self.marketplace.remove_from_cart(cart_id, "product1"), True)  
        self.assertEqual(self.marketplace.remove_from_cart(cart_id, "product1"), False)

    def test_place_order(self):
        producer_id = self.marketplace.register_producer()
        self.marketplace.publish(producer_id, "product1")
        self.marketplace.publish(producer_id, "product2")
        cart_id = self.marketplace.new_cart()
        self.marketplace.add_to_cart(cart_id, "product1")
        self.marketplace.add_to_cart(cart_id, "product2")
        self.assertEqual(self.marketplace.place_order(cart_id), ["product1", "product2"])    

   