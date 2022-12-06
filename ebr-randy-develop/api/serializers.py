from rest_framework import serializers
from core.models import Product

from django.contrib.auth.models import User


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Product
#         fields=[]
    
#     def create(self, validated_data):
#         user=User.objects.create(username=validated_data['username'])
#         user.set_password(validated_data['password'])
#         user.save()
#         return user





class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name','category','product_code','description','short_description','price']
        
 
    
    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
      instance.name=validated_data.get('name',instance.name)
      instance.roll=validated_data.get('category',instance.category)
      instance.city=validated_data.get('product_code',instance.product_code)
      instance.city=validated_data.get('description',instance.description)
      instance.city=validated_data.get('short_description',instance.short_description)
      instance.city=validated_data.get('price',instance.price)
      instance.save()
      return instance
     

    
    
    
      