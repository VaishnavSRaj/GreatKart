from django.db import models
from django.urls import reverse
from category.models import Category


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(max_length=250, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField(max_length=100)
    is_available = models.BooleanField(default=True)
    stock = models.IntegerField()
    product_image = models.ImageField(upload_to="photos/category")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse("product_detail", args=([self.category.slug, self.slug]))


variation_category_choice = (
    ("color", "color"),
    ("size", "size"),
)


class VariationManger(models.Manager):
    def colors(self):
        return super(VariationManger, self).filter(variation_category='color',is_active='True')
    def sizes(self):
        return super(VariationManger, self).filter(variation_category='size',is_active='True')


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(
        max_length=200, choices=variation_category_choice
    )
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects=VariationManger()
    
    def __str__(self):
        return self.variation_value
