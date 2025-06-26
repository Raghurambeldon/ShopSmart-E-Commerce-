from django.db import models
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True) 
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField( max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=1)
    image = models.ImageField( upload_to='images')
    desc = models.TextField()
    price = models.IntegerField()


    def __str__(self):
        return self.name
    
  #StaticMethod
    @staticmethod
    def get_category_id(get_id):
        if get_id:
            return Product.objects.filter(category=get_id)
        else:
            return Product.objects.all()
        

class Customer(models.Model):
    first_name = models.CharField( max_length=20)
    last_name = models.CharField( max_length=20)
    email = models.EmailField(max_length=254,unique=True)
    mobile = models.CharField(max_length=15,unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.email
    

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Link cart to the Customer
    product = models.ForeignKey(Product, on_delete=models.CASCADE)    # Link cart item to Product
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product in the cart
    
    class Meta:
        unique_together = ('customer', 'product')  # Ensure each product is unique per customer (no duplicates)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"


class Order(models.Model):
    # Define the payment method choices
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Card'),
        ('paypal', 'PayPal'),
    ]

    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')  # Example: 'Pending', 'Completed', 'Cancelled'
    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHOD_CHOICES,  # Use the choices here
        default='card'
    )

    def __str__(self):
        return f"Order {self.id} by {self.customer.email}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Store price at the time of checkout

    @property
    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"
