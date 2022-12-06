from django.db import models
from .review_category import ReviewCategory
from django.db.models.signals import pre_save, post_save
from django.db import models
from django.urls import reverse
from .users import User
from core.utils import category_brand_slugify, resize_image
# from .users import User 

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ReviewCategory,on_delete=models.CASCADE,null=True,blank=True)
    product_code = models.CharField(max_length=255)
    description = models.TextField()
    short_description = models.TextField()
    price= models.DecimalField(max_digits=10, decimal_places=2)
 
 
    def __str__(self):
        return str(self.name)


    class Meta:
        db_table = "name"
        indexes = [
			models.Index(fields=['id']),
			models.Index(fields=['name']),
			models.Index(fields=['product_code']),
            models.Index(fields=['description']),
            models.Index(fields=['short_description']),
            
		]