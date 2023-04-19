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


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField()


class ProductVariant(models.Model):
    name = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)







