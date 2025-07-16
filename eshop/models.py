from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=200)
	
	def __str__(self):
		return self.name

class Customer(AbstractUser):
	name = models.CharField(max_length=200, blank=True)
	email = models.EmailField(max_length=200,unique=True, null=True, blank=True)
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']	

	def __str__(self):
		return self.name


class Product(models.Model):
	name = models.CharField(max_length=200)
	price = models.FloatField()
	is_active = models.BooleanField(default=False,null=True, blank=True)
	in_stock = models.IntegerField(default=0, null=True, blank=True)
	image = models.ImageField(null=True, blank=True)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
	description = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)
	payment_method = models.CharField(max_length=50, default='Cash on Delivery')

	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self):
		return True

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	country = models.CharField(max_length=200, null=False, default='India')
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address
	
class OrderHistory(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	date_ordered = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Order {self.order.id} by {self.customer.name} on {self.date_ordered}" if self.customer else f"Order {self.order.id} on {self.date_ordered}"