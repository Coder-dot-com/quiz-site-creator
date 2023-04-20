from django.db import models
from quizCreation.models import UserQuiz
from ckeditor_uploader.fields import RichTextUploadingField
from multicurrency.models import Currency
# Create your models here.

class Product(models.Model):
    quiz = models.OneToOneField(UserQuiz, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000, null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    currency  = models.ForeignKey(Currency, null=True, blank=True, default=1, on_delete=models.SET_NULL)
    description = RichTextUploadingField(null=True, blank=True)
    require_shipping_information = models.BooleanField(default=False)

    def get_images(self):
        return ProductImage.objects.filter(product=self)



class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField()


class ProductVariant(models.Model):
    name = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('On hold', 'On hold'),
    )

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    number = models.CharField(max_length=200, null=True, blank=True)
    first_name = models.CharField(max_length=500, blank=True, null=True)
    last_name = models.CharField(max_length=500, blank=True, null=True)
    shipping_email = models.EmailField(max_length=500, blank=True, null=True)
    address_line_1 = models.CharField(max_length=150, blank=True, null=True)
    address_line_2 = models.CharField(max_length=500, blank=True, null=True)
    country = models.CharField(max_length=500, blank=True, null=True)
    city = models.CharField(max_length=500, blank=True, null=True)
    zip_postcode = models.CharField(max_length=500, blank=True, null=True)
    total = models.FloatField()
    currency_code = models.CharField(max_length=300)
    status = models.CharField(max_length=10, choices=STATUS, default="New")
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_intent_id = models.CharField(max_length=500, null=True, blank=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


    def full_address(self):
        return f"{self.address_line_1} {self.address_line_2}"


    def __str__(self):
        return self.email






