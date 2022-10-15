from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import SET_NULL

# Create your models here.

# "Product" model with its fields
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # reference to User model (who added Product)
    name = models.CharField(max_length=200, null=True, blank=True) # name of the product
    image = models.ImageField(null=True, blank=True, default='/placeholder.png') # image of the product
    brand = models.CharField(max_length=200, null=True, blank=True) # brand name of the product
    category = models.CharField(max_length=200, null=True, blank=True) # category of the product
    description = models.TextField(null=True, blank=True) # brief description of the product
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True) # rating
    numReviews = models.IntegerField(null=True, blank=True, default=0) # reviews of the product (in Number)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True) # price (decimal field)
    countInStock = models.IntegerField(null=True, blank=True, default=0) # number of product in stock
    createdAt = models.DateTimeField(auto_now_add=True) # date and time of creation of new product
    _id = models.AutoField(primary_key=True, editable=False) # auto incrementing unique id of the product

    def __str__(self):
        return self.name


# "Review" model with each review associated to Product
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True) # reference to the Product model
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # reference to User model (who has given reviews)
    name = models.CharField(max_length=200, null=True, blank=True) # name of the reviewer
    rating = models.IntegerField(null=True, blank=True, default=0) # rating of the review given
    comment = models.TextField(null=True, blank=True) # comment 
    _id = models.AutoField(primary_key=True, editable=False) # auto incrementing unique id of the review

    def __str__(self):
        return str(self.rating)


# "Order" model with informations like total price, tax price, payment and delivery information
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # reference to User model (who has placed the order)
    paymentMethod = models.CharField(max_length=200, null=True, blank=True) # payment method for this instance of order
    taxPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True) # tax price for this instance of order
    shippingPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True) # shipping price for this instance of order
    totalPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True) # total price for this instance of order
    isPaid = models.BooleanField(default=False) # boolean field that shows payment status (paid or not)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True) # date and time when the payment is done
    isDelivered = models.BooleanField(default=False) # boolean field that shows delivery status (delivered or not)
    deliveredAt = models.DateTimeField(auto_now_add=False, null=True, blank=True) # date and time when the order is delivered
    createdAt = models.DateTimeField(auto_now_add=True) # date and time when the ordered is placed
    _id = models.AutoField(primary_key=True, editable=False) # auto incrementing unique id of the order

    def __str__(self):
        return str(self.createdAt)

# "Order item" model - each object associated to Order
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True) # reference to Product model
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True) # reference to Order model (to which it is associated)
    name = models.CharField(max_length=200, null=True, blank=True) # name of the product
    qty = models.IntegerField(null=True, blank=True, default=0) # quantity of the product in order
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True) # price of the product
    image = models.CharField(max_length=200, null=True, blank=True) # image of the product
    _id = models.AutoField(primary_key=True, editable=False) # auto incrementing unique id of the order-item

    def __str__(self):
        return self.name


# "Shipping Address" model with informations like address, city, postal code, etc.
class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True) # Reference to Order model
    address = models.CharField(max_length=200, null=True, blank=True) # Address to which shipping is to be done
    city = models.CharField(max_length=200, null=True, blank=True) # City to which shipping is to be done
    postalCode = models.CharField(max_length=200, null=True, blank=True) # Postal code of the city
    country = models.CharField(max_length=200, null=True, blank=True) # Country
    shippingPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True) # Shipping price for this instance of order
    _id = models.AutoField(primary_key=True, editable=False) # auto incrementing unique id of the shipping address

    def __str__(self):
        return self.address