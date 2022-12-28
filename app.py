from xml.dom.pulldom import parseString
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os


app = Flask(__name__)                                           # initialize the app
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')      # DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)                                              # initialize DB
ma = Marshmallow(app)                                             # initialize MA. marshmallow = alternative to built-in serializer

# Product Class/Model
class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True)
  description = db.Column(db.String(200))
  price = db.Column(db.Float)
  qty = db.Column(db.Integer)

  def __init__(self, name, description, price, qty):
    self.name = name
    self.description = description
    self.price = price
    self.qty = qty

# Product Schema
class ProductSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'description', 'price', 'qty')

# Init schema
product_schema = ProductSchema(strict=True)
products_schema = ProductSchema(many=True, strict=True)

# Create a Product
@app.route('/product', methods=['POST'])              # @app.route = Flask decorator that lets us map URLS to our functions
def add_product():
  name = request.json['name']
  description = request.json['description']
  price = request.json['price']
  qty = request.json['qty']

  new_product = Product(name, description, price, qty)

  db.session.add(new_product)                        # add = prepares it to be written to DB
  db.session.commit()                                # commit = SQLalchemy function. Applies changes to DB

  return product_schema.jsonify(new_product)         # converts data to JSON format. Jsonify better than json.dumps. Jsonify returns response
                                                     # object, json.dumps doesn't (it only returns a string of JSON data)
# Get All Products
@app.route('/product', methods=['GET'])
def get_products():
  all_products = Product.query.all()                # equivalent to djangos .get. Goes DB > finds table named Product, and gets all data
  result = products_schema.dump(all_products)
  return jsonify(result.data)             

# Get Single Products
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
  product = Product.query.get(id)
  return product_schema.jsonify(product)

# Update a Product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
  product = Product.query.get(id)

  name = request.json['name']
  description = request.json['description']
  price = request.json['price']
  qty = request.json['qty']

  product.name = name
  product.description = description
  product.price = price
  product.qty = qty

  db.session.commit()

  return product_schema.jsonify(product)

# Delete Product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):    
  product = Product.query.get(id)
  db.session.delete(product)
  db.session.commit()

  return product_schema.jsonify(product)

# Run Server
if __name__ == '__main__':
  app.run(debug=True)

# OOP Principles

  # getter, setter, and deleter in python

  # @property = as decorator on top of a function to make it a getter function
  # return self.name

  # @name.setting = as decoratoron top of a function to make it a setter function
  # self.name = name 

  #@name.deleter 
  # del self.name

  # don't have to invoke setter, getter, and deleter like a normal function
  # print(customers[0].name)

  # del.customers[0].name


# Encapsulation - wrapping up data and functions together 
# Keeps data safe. Prevents access to methods/variables outside of a class 
# Creating a class is a form of encapsulation

# single underscore _ = private, but still can be used
# double underscore = __ = private, and can't be used 
# don't ever call these functions 


# Abstraction - handles complexity by hiding unnecessary information from user. This lets you implement even more complex logic
# on top of the abstracted information without having to understand the previous information.

# Creating an abstract class. This class can have abstract methods or non-abstract methods inside of it 

"""

from abc import ABC, abstractmethod

class ABSclass(ABC):                                # ABSclass has print and task function that are visible to user
    def print(self,x):
        print("Passed value: ", x)
    @abstractmethod
    def task(self):
        print("We are inside Absclass task")
 
class test_class(ABSclass):                               #test_class and example_class classes inherent from ABSclass 
    def task(self):
        print("We are inside test_class task")
 
class example_class(ABSclass):
    def task(self):
        print("We are inside example_class task")
 
test_obj = test_class()                             # creating instances of two child classes and calling task function
test_obj.task()                                     # task method/function from ABSclass never called
test_obj.print(100)                                 # when we call the print function ABSclass is invoked since print is not an absmethod
 
example_obj = example_class()                       # hidding functions of task inside both classes come into play 
example_obj.task()
example_obj.print(200)

"""

# tip: can't create instances of an Abstract Class


# Inheritance (Subclasses) : Let's you inherent attributes and methods from a parent class 
# Let's you add functionality without messing with the parent class. 

"""
class User:
  def log_data(self):
    print(self)

class Customer(User):
  pass

class Teacher(User):
  pass

"""

# You can call the child class( that has parent class passed in it), and it'll use the methods in the parent class
# In child classes (rememebr child classes not == nested classes, but classes that have inherited from parents)

"""
class Child(Parent):
  def __init__ (self):
    super().__init__(first, last, pay)       # let's you pass parents methods without having to type it in again

"""

# tip - don't set mutable(changable) data types in parameters of a method/function
# tip - never call functions with underscore before them, they're private.  class._method 

# issubclass() and isinstance() useful when working with inheritance


# Polymorphism - Define methods in the child class that have the same name as the methods in the parent class
# possible to modify a method in a child class that it has inherited from the parent class
# useful in cases where the method inherited from the parent class doesn’t quite fit the child class
# in such cases, we re-implement the method in the child class (method overriding)

# Polymorphism with Inheritance: 

"""

class Bird:
  def intro(self):
    print("There are many types of birds.")
     
  def flight(self):
    print("Most of the birds can fly but some cannot.")
   
class sparrow(Bird):
  def flight(self):
    print("Sparrows can fly.")
     
class ostrich(Bird):
  def flight(self):
    print("Ostriches cannot fly.")
     

"""

# Polymorphism with Functions and Objects :

"""

class India():
    def capital(self):
        print("New Delhi is the capital of India.")
  
    def language(self):
        print("Hindi is the most widely spoken language of India.")
  
    def type(self):
        print("India is a developing country.")
  
class USA():
    def capital(self):
        print("Washington, D.C. is the capital of USA.")
  
    def language(self):
        print("English is the primary language of USA.")
  
    def type(self):
        print("USA is a developed country.")
 
def func(obj):
    obj.capital()
    obj.language()
    obj.type()

"""