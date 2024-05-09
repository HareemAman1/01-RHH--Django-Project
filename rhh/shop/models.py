from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from shop.manager import UserManager


class DjangoUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    age = models.PositiveIntegerField(null=True, blank=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    postalcode = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        db_table = "django_user"

    def save(self, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        return super(DjangoUser, self).save(**kwargs)

    def __str__(self):
        return self.email


class UserOtpModel(models.Model):
    user = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, null=False, related_name='user_otp')
    code = models.IntegerField(null=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user


# USE this MODEL for Product
class ProductModel(models.Model):
    category = models.CharField(max_length=100)
    product_name = models.CharField(max_length=200, db_index=True)
    mg = models.CharField(max_length=20) #also add on product detail popup box
    product_picture = models.ImageField(upload_to="products", null=True)
    product_description = models.TextField(blank=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    product_stock = models.IntegerField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('product_name',)

    def __str__(self):
        return self.product_name


class Order(models.Model):
    user = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, null=False, related_name='user_order')
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

        
# Model for Information on item that is being placed in the order
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity


# Model for *Message Us* 
class MessageUs(models.Model):
    username = models.CharField(max_length=200, db_index=True)
    phonenum = models.CharField(max_length=20)
    useremail = models.EmailField(max_length=254)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
