from django.db import models
from django.urls import reverse


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    description = models.TextField(max_length=250, blank=True)
    category_image = models.ImageField(upload_to="photos/category")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def get_url(self):
        return reverse("product_by_category", args=[self.slug])

    def __str__(self):
        return self.category_name
