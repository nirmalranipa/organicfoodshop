from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Register(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    pass1 = models.CharField(max_length=10)
    pass2 = models.CharField(max_length=10)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Category(models.Model):
    cat_name = models.CharField(max_length=50)

    def __str__(self):
        return self.cat_name


class SubCategory(models.Model):
    catname = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcat_name = models.CharField(max_length=50)

    def __str__(self):
        return self.subcat_name


class Product(models.Model):
    cat_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcat_name = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.CharField(max_length=1000)
    product_image = models.ImageField(upload_to="media/%y/%m/%d")

    def __str__(self):
        return self.product_name


class Multiple_image(models.Model):
    p_image = models.ForeignKey(Product, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='media/%y/%m/%d')


class Cart(models.Model):
    prod_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    qty = models.IntegerField()
    price = models.IntegerField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.prod_name.product_name


class Contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    contact = models.IntegerField()
    subject = models.CharField(max_length=50)
    comment = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Chack(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=70)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=40)
    postcode = models.IntegerField()
    email = models.EmailField()
    phone = models.IntegerField()

    def __str__(self):
        return self.first_name


status_choices = [
    ("Pending", "Pending"),
    ("PLACED", "PLACED"),
    ("SHIPPED", "SHIPPED"),
    ("DELIVERED", "DELIVERED"),

]


class Order(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    product = models.CharField(max_length=50)
    address = models.ForeignKey(Chack, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    order = models.CharField(max_length=50, choices=status_choices, default='Pending')
